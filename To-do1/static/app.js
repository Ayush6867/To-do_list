// Selectors
const form = document.getElementById('create-todo-form');
const titleInput = document.getElementById('title-input');
const descriptionInput = document.getElementById('description-input');
const timeInput = document.getElementById('time-input');
const imagesInput = document.getElementById('images-input');
const todoList = document.getElementById('todo-list');

// Function to display success message
const showSuccessMessage = (message) => {
  const successMessage = document.createElement('p');
  successMessage.textContent = message;
  successMessage.classList.add('success-message');
  form.appendChild(successMessage);
};

// Function to display error message
const showErrorMessage = (message) => {
  const errorMessage = document.createElement('p');
  errorMessage.textContent = message;
  errorMessage.classList.add('error-message');
  form.appendChild(errorMessage);
};

// Function to create a new to-do item
const createTodo = async (e) => {
  e.preventDefault();

  // Reset error/success messages
  const errorMessages = document.getElementsByClassName('error-message');
  const successMessages = document.getElementsByClassName('success-message');
  if (errorMessages.length > 0) {
    errorMessages[0].remove();
  }
  if (successMessages.length > 0) {
    successMessages[0].remove();
  }

  const title = titleInput.value;
  const description = descriptionInput.value;
  const time = timeInput.value;
  const images = imagesInput.files;

  try {
    const response = await fetch('/todos', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title,
        description,
        time,
        images,
      }),
    });

    if (!response.ok) {
      const errorMessage = await response.text();
      throw new Error(errorMessage);
    }

    titleInput.value = '';
    descriptionInput.value = '';
    timeInput.value = '';
    imagesInput.value = '';

    showSuccessMessage('Todo created successfully');
    fetchTodos();
  } catch (error) {
    showErrorMessage(error.message);
  }
};

// Function to delete a to-do item
const deleteTodo = async (todoId) => {
  try {
    const response = await fetch(`/todos/${todoId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      const errorMessage = await response.text();
      throw new Error(errorMessage);
    }

    showSuccessMessage('Todo deleted successfully');
    fetchTodos();
  } catch (error) {
    showErrorMessage(error.message);
  }
};

// Function to fetch and display all to-do items
const fetchTodos = async () => {
  try {
    const response = await fetch('/todos');
    const todos = await response.json();

    todoList.innerHTML = '';

    todos.forEach((todo) => {
      const li = document.createElement('li');
      li.innerHTML = `
        <h3>${todo.title}</h3>
        <p>${todo.description}</p>
        <p>${todo.time}</p>
        <button onclick="deleteTodo(${todo.id})">Delete</button>
      `;

      todoList.appendChild(li);
    });
  } catch (error) {
    console.log(error);
  }
};

// Event listeners
form.addEventListener('submit', createTodo);

// Fetch initial todos on page load
fetchTodos();
