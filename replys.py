import datetime
import gspread


# Connect to Google Account
service_account = gspread.service_account(filename='gs_account.json')
# Connect to Google Sheets
sheets = service_account.open('Ai workflow')
orders_task_list = sheets.worksheet('OrdersTaskList')
orders = sheets.worksheet('Orders')

def process_message(messages, user):
    reply = []
    delivery_note = 'تحضير وإرسال فوري'
    
    # Check if Quotation
    if messages[0][2] == '1':
        
        # Get current time
        now = datetime.datetime.now()
        
        # Get all column names
        column_names = orders_task_list.row_values(1)

        # Create a dictionary with empty values
        orders_task_list_default = dict.fromkeys(column_names, '')
        
        try:
            int(messages[-1])
            for message in messages:
                if orders_task_list.find(message, in_column=5) or orders.find(message, in_column=1):
                    reply.append(f"الطلبية رقم {message} مكررة")
                else:
                    created_time = now.strftime("%d/%m/%Y %I:%M %p")
                    update = {'Created by': user, 'Create DateTime': created_time, 'Quotation': message, 'Delivery_Note': delivery_note}
                    update = dict(orders_task_list_default, **update)
                    update = list(update.values())
                    orders_task_list.append_row(update, value_input_option='USER_ENTERED')
                    reply.append(f"تم إضافة الطلبية {message} وجاري العمل على المطلوب")
        except Exception:
            delivery_note = messages[-1]
            for message in messages[:-1]:
                if orders_task_list.find(message, in_column=5) or orders.find(message, in_column=1):
                    reply.append(f"الطلبية رقم {message} مكررة")
                else:
                    created_time = now.strftime("%d/%m/%Y %I:%M %p")
                    update = {'Created by': user, 'Create DateTime': created_time, 'Quotation': message, 'Delivery_Note': delivery_note}
                    update = dict(orders_task_list_default, **update)
                    update = list(update.values())
                    orders_task_list.append_row(update, value_input_option='USER_ENTERED')
                    reply.append(f"تم إضافة الطلبية {message} وجاري العمل على المطلوب")
    for message in messages:
    
        # English Response 
        if message in ("هلا"):
            reply.append('هلا')
        elif message.lower() in ("hi"):
            reply.append('Hey!')
    
    print('\n'.join(reply))
    return '\n'.join(reply)



# message = ['52119010', '52119011', 'تحضير']
# if message[0][2] == '1':
#     try:
#         int(message[-1])
#         for msg in message:
#             print(msg)
#     except Exception:
#         for msg in message[:-1]:
            
#             print(Exception)
