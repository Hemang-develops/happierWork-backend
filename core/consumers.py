import os
import secrets
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import aiofiles
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, 'components/budget/data.json')

class DashboardConsumer(AsyncWebsocketConsumer):
    logged_in_users = {};
    async def connect(self):
        await self.channel_layer.group_add("dashboard", self.channel_name)
        await self.accept()
        
        await self.send_login_update()

    async def disconnect(self, close_code):
        user_id = self.scope['user'].username
        if user_id in self.logged_in_users:
            del self.logged_in_users[user_id]
            await self.send_login_update()

        await self.channel_layer.group_discard("dashboard", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        data = [item.strip("""'""'""") for item in data.strip( "'['[""]']''").split(",")]
        # Split the string by commas and strip extra quotes
        try:
            # Check if data is a list
            if isinstance(data, list):
                action, element_id = data[0], data[1]
                print(action)
                if action.strip() == "delete":
                    await self.deleteBudgetData(element_id)
                elif action.strip() == "add":
                    entry_id = self.generate_id()
                    form_data = {
                        "id":entry_id,"designation": data[1],"department": data[2],"budget": data[3],"location": data[4],
                        "lastUpdated": ["Admin",self.get_current_datetime()]
                    }
                    await self.channel_layer.group_send(
                        "positions_group",
                        {
                            "type": "broadcast_message",
                            "message": form_data
                        }
                    )
                    await self.addBudgetData(form_data)
                elif action.strip() == "login":
                    self.logged_in_users[element_id] = {'status': 'online'}
                    await self.send_login_update()
                    await self.channel_layer.group_send(
                        "dashboard",
                        {
                            'type': 'broadcast_message',
                            'status': 'tracking successfully',
                            'loginData': element_id
                        }
                    )
                elif action.strip() == "tracking":
                    await self.channel_layer.group_send(
                        "dashboard",
                        {
                            'type': 'broadcast_message',
                            'status': 'tracking successfully',
                            'elementID': element_id
                        }
                    )
            else:
                print(f"Expected a list, but received {type(data)}: {data}")

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON data'
            }))
            return

        await self.send(text_data=json.dumps({
            "status": "Data processed"
        }))

    def generate_id(self, length=15):
        return secrets.token_hex(length // 2)
    
    def get_current_datetime(self):
        """Returns the current date and time in the required format"""
        return datetime.now().strftime("%b %d, %Y %I:%M %p")  # Example: 'Jun 4, 2022 11:33 am'

    async def send_login_update(self):
        await self.channel_layer.group_send(
            "dashboard",
            {
                'type': 'broadcast_login_update',
                'logged_in_users': self.logged_in_users
            }
        )
    
    async def broadcast_login_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'login_update',
            'logged_in_users': event['logged_in_users']
        }))
    
    async def broadcast_message(self, event):
        if event['message']:
            message = event['message']
            await self.send(text_data=json.dumps(message))
        await self.send(text_data=json.dumps({
            'status': event['status'],
            'elementID': event.get('elementID'),
            'loginData': event.get('loginData')
        }))

    async def dashboard_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def addBudgetData(self, form_data):
        try:
            print(f"Attempting to add entry: {form_data}")
            
            async with aiofiles.open(DATA_FILE, mode='r') as file:
                data = json.loads(await file.read())

            if not isinstance(data, list):
                data = []

            data.insert(0, form_data)

            async with aiofiles.open(DATA_FILE, mode='w') as file:
                await file.write(json.dumps(data, indent=4))

            print(f"Entry added successfully: {form_data}")

            await self.send(text_data=json.dumps({
                "status": "Data added successfully",
                "entry": form_data
            }))
            return

        except Exception as e:
            print(f"Error while adding entry: {str(e)}")
            await self.send(text_data=json.dumps({
                "error": f"Failed to add data: {str(e)}"
            }))
            return


    async def deleteBudgetData(self, entry_id):
        print(f"Attempting to delete entry with ID: {entry_id}")
        
        try:
            print('here')
            async with aiofiles.open(DATA_FILE, mode='r') as file:
                data = json.loads(await file.read())
                data = [entry for entry in data if entry.get('id') != entry_id]

            # Write the updated data back to the file
                async with aiofiles.open(DATA_FILE, mode='w') as file:
                    await file.write(json.dumps(data, indent=4))

                print(f"Entry with ID {entry_id} deleted successfully.")

                await self.send(text_data=json.dumps({
                    "status": "Data deleted successfully"
                }))
                return
            
        except Exception as e:
            print(f"Error while deleting entry: {str(e)}")

            await self.send(text_data=json.dumps({
                "error": f"Failed to delete data: {str(e)}"
            }))
            return
