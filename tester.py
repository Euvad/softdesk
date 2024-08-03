import requests
from colorama import Fore, init

# Initialize colorama for colored output
init(autoreset=True)

# Define base URL for API endpoints
BASE_URL = "http://localhost:8000/api/"

# Define test users and other data
TEST_USER = {
    "username": "",  # We'll set this dynamically using input()
    "email": "testuser@example.com",
    "password": "securepassword123",
    "age": 20,
    "can_be_contacted": True,
    "can_data_be_shared": False
}

TEST_PROJECT = {
    "name": "New Project",
    "description": "Project description",
    "type": "BACKEND"
}

TEST_ISSUE = {
    "title": "Test Issue",
    "description": "Issue description",
    "tag": "BUG",
    "priority": "HIGH",
    "status": "TODO"
}

TEST_COMMENT = {
    "description": "This is a test comment."
}

# Function to print test result with debug information
def print_result(test_name, response, success):
    if success:
        print(f"{Fore.GREEN}{test_name} - OK")
    else:
        print(f"{Fore.RED}{test_name} - FAIL")
        print(f"{Fore.YELLOW}Status Code: {response.status_code}")
        print(f"{Fore.YELLOW}Response: {response.text}")

# Test creating a user
def test_create_user():
    url = BASE_URL + "users/"
    response = requests.post(url, json=TEST_USER)
    if response.status_code == 400 and "username" in response.json():
        print(f"{Fore.YELLOW}User already exists, proceeding with existing user.")
        return True
    print_result("Create User", response, response.status_code == 201)
    return response.status_code == 201

# Test obtaining a JWT token
def test_obtain_token():
    url = BASE_URL + "token/"
    data = {"username": TEST_USER["username"], "password": TEST_USER["password"]}
    response = requests.post(url, json=data)
    print_result("Obtain Token", response, response.status_code == 200)
    if response.status_code == 200:
        return response.json().get("access")
    return None

# Test listing users
def test_list_users(token):
    url = BASE_URL + "users/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print_result("List Users", response, response.status_code == 200)

# Test creating a project
def test_create_project(token):
    url = BASE_URL + "projects/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, json=TEST_PROJECT, headers=headers)
    print_result("Create Project", response, response.status_code == 201)
    if response.status_code == 201:
        return response.json().get("id")
    else:
        # If creation fails, try listing projects to use an existing one
        return test_get_existing_project_id(token)

# Get an existing project ID if creation fails
def test_get_existing_project_id(token):
    url = BASE_URL + "projects/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print_result("List Projects", response, response.status_code == 200)
    if response.status_code == 200:
        projects = response.json()
        if projects:
            return projects[0]["id"]  # Return the first project's ID if available
    return None

# Test creating an issue
def test_create_issue(token, project_id):
    url = BASE_URL + "issues/"
    headers = {"Authorization": f"Bearer {token}"}
    issue_data = TEST_ISSUE.copy()
    issue_data["project"] = project_id
    issue_data["assignee"] = 1  # Assuming user ID 1 exists; adjust if necessary
    response = requests.post(url, json=issue_data, headers=headers)
    print_result("Create Issue", response, response.status_code == 201)
    if response.status_code == 201:
        return response.json().get("id")
    else:
        # Log error if issue creation fails
        print(f"Create Issue - FAIL: {response.text}")
        return test_get_existing_issue_id(token)

# Get an existing issue ID if creation fails
def test_get_existing_issue_id(token):
    url = BASE_URL + "issues/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print_result("List Issues", response, response.status_code == 200)
    if response.status_code == 200:
        issues = response.json()
        if issues:
            return issues[0]["id"]  # Return the first issue's ID if available
    return None

# Test creating a comment
def test_create_comment(token, issue_id):
    url = BASE_URL + "comments/"
    headers = {"Authorization": f"Bearer {token}"}
    comment_data = TEST_COMMENT.copy()
    comment_data["issue"] = issue_id
    response = requests.post(url, json=comment_data, headers=headers)
    print_result("Create Comment", response, response.status_code == 201)
    if response.status_code == 201:
        return response.json().get("id")
    else:
        # Log error if comment creation fails
        print(f"Create Comment - FAIL: {response.text}")

# Main function to run all tests
def run_tests():
    # Prompt for username input
    TEST_USER["username"] = input("Enter a username for testing: ")

    if not test_create_user():
        print("Exiting due to user creation failure.")
        return
    token = test_obtain_token()
    if token:
        test_list_users(token)

        # Test project operations
        project_id = test_create_project(token)
        if project_id:
            # Test issue operations
            issue_id = test_create_issue(token, project_id)
            if issue_id:
                # Test comment operations
                test_create_comment(token, issue_id)

if __name__ == "__main__":
    run_tests()
