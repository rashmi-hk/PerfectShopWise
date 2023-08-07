
function createDropDown(){
return `
        <li class="nav-item dropdown"  {% if not user_is_authenticated %}hidden{% endif %}>>
          <a class="nav-link  dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
         <span id= "user-detail" class="text-white">{{user_name}}</span>
              <i class='fas fa-user-alt' style='font-size:24px;color:red'></i>

          </a>
            <ul class="dropdown-menu " id="profileDropdownContainer" style="background-color:gray;">
                  <li><a class="dropdown-item" href="{% url  'register_variant' variant=1 %}">Profile</a></li>
                  <li><a class="dropdown-item" href="{% url 'order' %}">Order History</a></li>
                  <li><a class="dropdown-item" href="{% url 'logout' %}">Logout</a></li>
                </ul>

        </li>`
}




function getAuthenticationStatus() {
   console.log("Inside   getAuthenticationStatus")
    fetch('/check_user', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',

        }
    })
    .then(response => response.json())
    .then(data => {
        const isAuthenticated = data.user_is_authenticated;
        console.log("--user status",isAuthenticated)
        // Do something with the userIsAuthenticated value

//dropDownContainer.appendChild(childElement)



          if (isAuthenticated) {
              console.log("is athenticated")
              let dropDownContainer = document.getElementById('cartContainer')
              let childElement = createDropDown()

              dropDownContainer.insertAdjacentHTML("beforeend",childElement)
          }
          else {
            console.log("Not athenticated")
}
    })
    .catch(error => {
        // Handle any errors
        console.error('Error getting authentication status:', error);
    });
}

// Call the function to get authentication status on page load
getAuthenticationStatus();
