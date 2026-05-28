*{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body{
    display: flex;
    flex-direction: row;
}

nav{
    width: 30%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: rgb(8, 8, 117);
}


.logo img {
  max-width: 130px;
  height: auto;
  display: block;
}

.navRight{
    display: flex;
    gap: 20px;
}

.navRight a{
    text-decoration: none;
    color: #fff;
    /* border: 2px solid red; */
    background-color: rgb(19, 19, 183);
    padding: 5px 10px;
    border-radius: 10px;
    cursor: pointer;
}

main{
    height: 82vh;
    width: 70%;
    background-image: url("{% static 'image/nick-morrison-FHnnjk1Yj7Y-unsplash.jpg' %}");
}

footer{
    background-color: rgb(8, 8, 117);
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
}

footer p{
    color: #fff;
}




<nav>
              

         <a href="/" class="logo">
        {% comment %} <img src="{% static 'image/logo.png' %}" alt="smartstudy Logo"> {% endcomment %}
        </a> 
        <div class="navRight">
            <a href="/">Dashboard</a>
            <a href="/students/">student</a>
            <a href="/about/">About</a>
            <a href="/courses/">course</a>
        </div>
        <a href="{% url 'login' %}">Login</a>
        <a href="{% url 'register' %}">Register</a>
    </nav>

    <main>

        {% if messages %}
            {% for messages in messages %}
                <div class='alert alert-{{ message.tags }}'>
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}

        {% block content%}
        {% endblock %}















        {% load static %}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %} SmartStudy {% endblock %}</title>
    <link rel='stylesheet' href="{% static 'css/main.css' %}"> 

</head>
<body>
    <script  src="{% static 'js/main.js' %}"></script>

    <nav>

        <a href="/" class="logo"><img src="{% static 'image/logo.png' %}" alt="smartstudy Logo"> </a> 
            <h2>SmartStudy</h2>
                  
            <div class="nav-links">
            <a href="/">Home</a>
    

            {% if request.user.is_authenticated and request.user.is_student %}
            <!-- show only to logged-in users -->

                <span style="color: white; padding: 8px 16px;">Hello, {{ request.user.username }}</span>

                <!-- Corrected logout: Must use POST for Django 5.0+ -->
                <form action="{% url 'logout' %}" method="post" style="display: inline;">
                {% csrf_token %}
                <button type="submit">Logout</button>
                </form>

                <form action="{% url 'logout' %}" method="post" style="display: inline;">
                    {% csrf_token %}
                    <button type="submit">Logout</button>
                </form>
            {% elif request.user.is_authenticated and request.user.is_staff_member %}    
                <a href="{% url 'staff_dashboard' %}">🏠 Dashboard</a>
            {% comment %} <a href="{% url 'staff_student_profiles' %}">👥 Student Profiles</a> {% endcomment %}
            {% comment %} <a href="{% url 'staff_add_course' %}">📚 Add Course</a> {% endcomment %}
            {% comment %} <a href="{% url 'staff_add_grade' %}">🎓 Add Grade</a> {% endcomment %}
            {% comment %} <a href="{% url 'staff_view_submissions' %}">📝 View Submissions</a> {% endcomment %}
            {% comment %} <a href="{% url 'staff_add_announcement' %}">📢 Add Announcement</a> {% endcomment %}
                <span style="color: white; padding: 8px 16px;">Hello, {{ request.user.username }}</span>


                <form method="post" action="{% url 'logout' %}" style="display:inline;">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-link" style="padding:0; margin:0; border:none; background:none;">
                        Logout
                    </button>
                </form>

            {% else %}
                <!-- Shown only to loggged-out visitors -->
                <a href="{% url 'login' %}">Login</a>
                <a href="{% url 'register' %}">Register</a>
            {% endif %}
        </div>         
    </nav>



        
        <!-- Sidebar: visible to students and staff -->


    <nav class="sidebar-nav">
        {% if request.user.is_student %}
            <a href="{% url 'student_dashboard' %}">🏠 Dashboard</a>
            <a href="{% url 'student_courses' %}">📚 Courses</a>
            <a href="{% url 'student_assignments' %}">📝 Assignments</a>
            <a href="{% url 'student_profile' %}">👤 Profile</a>
{% comment %} 
        {% elif request.user.is_staff_member %}
            <a href="{% url 'staff_dashboard' %}">🏠 Dashboard</a> {% endcomment %}
            {% comment %} <a href="{% url 'staff_student_profiles' %}">👥 Student Profiles</a> {% endcomment %}
            {% comment %} <a href="{% url 'staff_add_course' %}">📚 Add Course</a> {% endcomment %}
            {% comment %} <a href="{% url 'staff_add_grade' %}">🎓 Add Grade</a> {% endcomment %}
            {% comment %} <a href="{% url 'staff_view_submissions' %}">📝 View Submissions</a> {% endcomment %}
            {% comment %} <a href="{% url 'staff_add_announcement' %}">📢 Add Announcement</a> {% endcomment %}
        {% comment %} {% endif %} {% endcomment %}
    </nav>

{% endif %}


    <main>

        {% if messages %}
            {% for message in messages %}
                <div class='alert alert-{{ message.tags }}'>
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}

        {% block content%}
        {% endblock %}
        <footer>
            <p>copyright &copy; smartstudy</p>
        </footer>
    </main>
    
    
    
</body>


</html>