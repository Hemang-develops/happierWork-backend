# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("dashboard", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("dashboard", self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON data'
            }))
            return
        
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    print(f"Received item: {item}")
                else:
                    print("Expected a dictionary, but received something else.")
        else:
            print("Expected a list, but received something else.",data)
            if data[0] == 'delete':
                print('del')
                # def delete_position(request, position_id):
                #     if request.method == 'DELETE':
                #         try:
                #             position = BudgetData.objects.get(id=position_id)
                #             position.delete()
                #             return JsonResponse({'message': 'Position deleted successfully'}, status=200)
                #         except BudgetData.DoesNotExist:
                #             return JsonResponse({'error': 'Position not found'}, status=404)
                #     return JsonResponse({'error': 'Invalid request method'}, status=400)

        
        await self.send(text_data=json.dumps({
            "status": "Data processed"
        }))

    async def dashboard_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
