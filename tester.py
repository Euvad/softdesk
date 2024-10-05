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
    "status": "TODO",
    "assignee": None  # We'll set this later
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

# Test creating a user and return its ID
def test_create_user():
    url = BASE_URL + "users/"
    response = requests.post(url, json=TEST_USER)
    if response.status_code == 201:
        user_id = response.json().get('id')
        print_result("Create User", response, True)
        return user_id
    elif response.status_code == 400 and "username" in response.json():
        print(f"{Fore.YELLOW}User already exists, proceeding with existing user.")
        return None  # In this case, you might want to get the user ID manually
    print_result("Create User", response, False)
    return None

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

# Test adding the user as a contributor to the project (without role)
def test_add_contributor(token, project_id, user_id):
    url = f"{BASE_URL}projects/{project_id}/contributors/"
    headers = {"Authorization": f"Bearer {token}"}
    contributor_data = {
        "user": user_id,
        "role": "CONTRIBUTOR"  # Adjust as necessary
    }
    response = requests.post(url, json=contributor_data, headers=headers)
    print_result("Add Contributor", response, response.status_code == 201)
    return response.status_code == 201

# Test creating an issue and directly return its ID
def test_create_issue(token, project_id):
    url = f"{BASE_URL}projects/{project_id}/issues/"
    headers = {"Authorization": f"Bearer {token}"}
    issue_data = TEST_ISSUE.copy()
    issue_data["assignee"] = 1  # Assuming user ID 1 exists; adjust if necessary
    response = requests.post(url, json=issue_data, headers=headers)
    
    print_result("Create Issue", response, response.status_code == 201)
    
    if response.status_code == 201:
        issue_id = response.json().get('id')  # Get the ID of the created issue
        return issue_id
    else:
        print(f"Create Issue - FAIL: {response.text}")
        return None

# Test listing issues for a project
def test_list_issues_for_project(token, project_id):
    url = f"{BASE_URL}projects/{project_id}/issues/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print_result(f"List Issues for Project {project_id}", response, response.status_code == 200)

# Test creating a comment
def test_create_comment(token, project_id, issue_id):
    url = f"{BASE_URL}projects/{project_id}/issues/{issue_id}/comments/"
    headers = {"Authorization": f"Bearer {token}"}
    comment_data = TEST_COMMENT.copy()
    response = requests.post(url, json=comment_data, headers=headers)
    print_result("Create Comment", response, response.status_code == 201)
    if response.status_code == 201:
        return response.json().get("id")
    else:
        # Log error if comment creation fails
        print(f"Create Comment - FAIL: {response.text}")
        return None

# Test listing comments for an issue
def test_list_comments_for_issue(token, project_id, issue_id):
    url = f"{BASE_URL}projects/{project_id}/issues/{issue_id}/comments/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print_result(f"List Comments for Issue {issue_id}", response, response.status_code == 200)

# Test editing an issue without being the author
def test_edit_issue(token, project_id, issue_id):
    url = f"{BASE_URL}projects/{project_id}/issues/{issue_id}/"
    headers = {"Authorization": f"Bearer {token}"}
    updated_data = {
        "title": "Updated Issue Title",
        "description": "Updated description",
        "tag": "FEATURE",
        "priority": "MEDIUM",
        "status": "IN_PROGRESS",
        "assignee": 1  # Adjust as necessary
    }
    response = requests.put(url, json=updated_data, headers=headers)
    print_result("Edit Issue (non-author)", response, response.status_code == 403)  # Should fail

# Test deleting an issue without being the author
def test_delete_issue(token, project_id, issue_id):
    url = f"{BASE_URL}projects/{project_id}/issues/{issue_id}/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    print_result("Delete Issue (non-author)", response, response.status_code == 403)  # Should fail

# Test editing a comment without being the author
def test_edit_comment(token, project_id, issue_id, comment_id):
    url = f"{BASE_URL}projects/{project_id}/issues/{issue_id}/comments/{comment_id}/"
    headers = {"Authorization": f"Bearer {token}"}
    updated_data = {
        "description": "Updated comment description"
    }
    response = requests.put(url, json=updated_data, headers=headers)
    print_result("Edit Comment (non-author)", response, response.status_code == 403)  # Should fail

# Test deleting a comment without being the author
def test_delete_comment(token, project_id, issue_id, comment_id):
    url = f"{BASE_URL}projects/{project_id}/issues/{issue_id}/comments/{comment_id}/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    print_result("Delete Comment (non-author)", response, response.status_code == 403)  # Should fail

# Main function to run all tests
def run_tests():
    # Prompt for username input
    TEST_USER["username"] = input("Enter a username for testing: ")

    user_id = test_create_user()
    if user_id is None:
        print("User creation failed or user already exists.")
        return

    token = test_obtain_token()
    if token:
        test_list_users(token)

        # Test project operations
        project_id = test_create_project(token)
        if project_id:
            # Add the user as a contributor to the project
            if test_add_contributor(token, project_id, user_id):
                # Test issue operations
                issue_id = test_create_issue(token, project_id)
                if issue_id:
                    # Test comment operations
                    comment_id = test_create_comment(token, project_id, issue_id)

                    # Test editing and deleting issue and comment without being the author
                    if issue_id:
                        test_edit_issue(token, project_id, issue_id)
                        test_delete_issue(token, project_id, issue_id)
                    
                    if comment_id:
                        test_edit_comment(token, project_id, issue_id, comment_id)
                        test_delete_comment(token, project_id, issue_id, comment_id)

                    # Test listing issues for the project
                    test_list_issues_for_project(token, project_id)

                    # Test listing comments for the issue
                    test_list_comments_for_issue(token, project_id, issue_id)
            else:
                print("Failed to add contributor to the project.")
        else:
            print("Project creation failed.")

if __name__ == "__main__":
    run_tests()
