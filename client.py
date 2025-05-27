import socket

#Constants
HOST = '127.0.0.1'  # The IP address of the server
PORT = 65432  # The port number used for communication
BUFFER_SIZE = 1024  # The size of the buffer for receiving data
FALSE_RESPONSE = "False"  # The response indicating an invalid employee ID


def send_request(client_socket, query):
    #send to the server
    client_socket.sendall(query.encode())

def receive_response(client_socket):
    #get response from the server
    return client_socket.recv(BUFFER_SIZE).decode()

def menu_system(employee, client_socket):
    #query broken into 4 parts  employee id, main query, sub query and year query
    #this gets the main query and sub query from the user, then calles the related function
    main_query = input("Salary (S) or Annual Leave (L) Query? ").upper()
    #error checking to make sure the user enters a valid query
    if main_query not in ['S', 'L']:
        print("Sorry... I don’t recognise that query")
        return

    if main_query == 'S':  
        sub_query = input("Current salary (C) or total salary (T) for year? ").upper()
        handle_salary_sub_query(employee, client_socket, sub_query)
    elif main_query == 'L':
        sub_query = input("Current Entitlement (C) or Leave taken for year (Y)? ").upper()
        handle_leave_sub_query(employee, client_socket, sub_query)

 #this defines the query further by asking for the year if the user wants the total salary for the year
def handle_salary_sub_query(employee, client_socket, sub_query):
    #error checking to make sure the user enters a valid query
    if sub_query not in ['C', 'T']:
        print("Sorry... I don’t recognise that query")
        return

    if sub_query == 'T':
        year_query = input("What Year? ").upper()
        query = f"{employee},S,{sub_query},{year_query}"
    else:
        query = f"{employee},S,{sub_query}"
    #the full query is sent to the server and the response is returned and printed
    send_request(client_socket, query)
    response = receive_response(client_socket)
    print(response)

#this defines the query further by asking for the year if the user wants the leave taken for the year
def handle_leave_sub_query(employee, client_socket, sub_query):
    #error checking to make sure the user enters a valid query
    if sub_query not in ['C', 'Y']:
        print("Sorry... I don’t recognise that query")
        return

    if sub_query == 'Y':
        year_query = input("What Year? ").upper()
        query = f"{employee},L,{sub_query},{year_query}"
    else:
        query = f"{employee},L,{sub_query}"

    #the full query is sent to the server and the response is returned and printed
    send_request(client_socket, query)
    response = receive_response(client_socket)
    print(response)

def main():
    print("HR System 1.0")
    print("-" * 50)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            # Connect to server
            client_socket.connect((HOST, PORT))
            while True:
                # Get employee id as input
                emp_id = input("What is the employee id? ")
                #send employee id as request to the server and get back the reponse
                send_request(client_socket, emp_id)
                response = receive_response(client_socket)

                #check if the  employee iD is valid if it isnt then ask for the employee id again else go to the menu system
                if response == FALSE_RESPONSE:
                    print("Sorry... I don’t recognise that employee id")
                    continue
                else:
                    menu_system(emp_id, client_socket)

                choice = input("Would you like to continue (C) or exit (X)? ").upper()
                if choice == 'X':
                    print("Goodbye")
                    break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
