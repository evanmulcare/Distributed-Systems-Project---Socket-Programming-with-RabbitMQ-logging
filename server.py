from tinydb import TinyDB
from Employee import Employee
import socket
import pika  

import selectors
sel = selectors.DefaultSelector() #allows the server to handle multiple clients at once

#Constants
HOST = '127.0.0.1'  # The IP address of the server
PORT = 65432  # The port number used for communication
BUFFER_SIZE = 1024  # The size of the buffer for receiving data
FALSE_RESPONSE = "False"  # The response indicating an invalid employee ID

# Initialize TinyDB
db = TinyDB('employees_db.json') 
employees_table = db.table('employees') # Get the table of employees
employees = []
for employee_dict in employees_table.all(): # Get all the employees from the database
    employee = Employee(**employee_dict) # Unpack the dictionary
    employees.append(employee) # Add the employee to the list

# Connect to RabbitMQ from localhost
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# Create a channel
channel = connection.channel()
# Declare the activity_log queue
channel.queue_declare(queue='activity_log')

#function to validate the input query from the client
def query_salary(data):
    #split the query into 4 parts and assign them as empty strings if there is no value
    values = data.split(',')
    employee_id = values[0] if values else ""
    main_query = values[1] if len(values) > 1 else ""
    sub_query = values[2] if len(values) > 2 else ""
    year_query = values[3] if len(values) > 3 else ""

    #.define and send the log message to the activity log queue in RabbitMQ
    log_message = f"Employee ID {employee_id}, Command: {main_query} {sub_query} {year_query}, IP address: {HOST}"
    channel.basic_publish(exchange='', routing_key='activity_log', body=log_message)

    #validate the employee id
    employee = validate_employee(employee_id)
    #if the employee id is valid, call the request_menu_response function, else return false response to the client
    if employee:
        response = request_menu_response(employee, main_query, sub_query, year_query)
        return response
    else:
        return FALSE_RESPONSE
    
def validate_employee(employee_id):
    for employee in employees: # Loop through all the employees
        if employee.emp_id == employee_id: # Check if the employee ID matches
            return employee # Return the employee object
    return None # Return None if no employee ID matches

#function to handle the request from the client, send back the employee information based on the query
def request_menu_response(employee, main_query, sub_query, year_query):
    if main_query == 'S':
        if sub_query == 'C':
            return f"{employee.get_employee_name()}\n{employee.get_current_salary()}"
        elif sub_query == 'T':
            return f"{employee.get_employee_name()}\n{employee.get_total_salary_for_year(year_query)}"
    elif main_query == 'L':
        if sub_query == 'C':
            return f"{employee.get_employee_name()}\n{employee.get_current_annual_leave_entitlement()}"
        elif sub_query == 'Y':
            return f"{employee.get_employee_name()}\n{employee.get_leave_taken(year_query)}"
    else:
        return "Sorry... I don’t recognize that query"

# Function to accept incoming connections and register them with the selector
def accept_connection(sock, mask):
    connection, address = sock.accept()
    print(f"Accepted connection from {address}")
    connection.setblocking(False)
    sel.register(connection, selectors.EVENT_READ, read_data) #read_data is the callback function, it will be called when the client sends data to the server

# Function to read data from connected clients and process the requests
def read_data(connection, mask):
    data = connection.recv(BUFFER_SIZE).decode()
    if data:
        response = query_salary(data) #query_salary is called to validate the query and return the response
        connection.sendall(response.encode())
    else:
        sel.unregister(connection) #unregister the connection from the selector
        connection.close() #close the connection

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
         # Bind the socket to the host and port
        server_socket.bind((HOST, PORT))
        # Enable the server to accept incoming connections
        server_socket.listen()
        print(f"Server listening on port {PORT}...")

        #allow mutliple connections concurrently by setting the socket to non-blocking
        server_socket.setblocking(False)
        # set accept_connection as the callback function for the server socket, when  a new connection is made the callback function will be called
        sel.register(server_socket, selectors.EVENT_READ, accept_connection)

        # loop to wait for events to occur and trigger the callback functions
        while True:
            # Wait for events to occur on registered sockets
            events = sel.select()
            # Iterate over the events and handle each one
            for key, mask in events:
                # Get the callback function associated with the event
                callback = key.data
                # Call the callback function 
                callback(key.fileobj, mask)

if __name__ == "__main__":
    main()
