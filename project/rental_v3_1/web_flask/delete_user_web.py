from flask import Flask, render_template_string

app = Flask(__name__)

# HTML jako string – tu wklejamy odpowiednik Twojego widgetu
TEMPLATE = """
<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <title>Usuń użytkowników</title>
  <style>
    body {
      background-color: #2e2e2e;
      color: #eee;
      font-family: Arial, sans-serif;
      font-size: 16px;
      padding: 20px;
    }
    h1 { font-size: 24px; color: #A9C1D9; text-align: center; }
    ul { list-style: none; padding: 0; margin: 10px 0; background-color: #444;
         border-radius: 8px; max-height: 300px; overflow-y: auto; }
    li { padding: 8px 12px; border-bottom: 1px solid #555; cursor: pointer; }
    li:hover { background-color: #666; }
    button {
      font-size: 18px; padding: 8px 12px;
      border: none; border-radius: 10px;
      margin: 5px; cursor: pointer;
    }
    .green { background-color: darkgreen; color: white; }
    .brown { background-color: brown; color: white; }
    #summary { margin-top: 15px; color: white; display: none; }
    .buttons { margin-top: 15px; }
  </style>
</head>
<body>

  <h1>=== Przegląd klientów wypożyczalni niemających wypożyczeń ===</h1>

  <ul id="userList"></ul>

  <button id="showBtn" class="green">Pokaż</button>

  <p id="summary"></p>

  <div class="buttons">
    <button id="cancelBtn" class="brown" style="display:none;">Anuluj</button>
    <button id="deleteBtn" class="green" style="display:none;">Usuń użytkownika</button>
  </div>

  <script>
    const users = [
      {id: 1, first_name: "Jan", last_name: "Kowalski", login: "janko"},
      {id: 2, first_name: "Anna", last_name: "Nowak", login: "aneczka"},
    ];

    const userList = document.getElementById("userList");
    const summary = document.getElementById("summary");
    const showBtn = document.getElementById("showBtn");
    const cancelBtn = document.getElementById("cancelBtn");
    const deleteBtn = document.getElementById("deleteBtn");

    let selectedUserId = null;

    function populateUsers() {
      userList.innerHTML = "";
      if (users.length === 0) {
        alert("Brak klientów bez aktywnego wypożyczenia.");
        return;
      }
      users.forEach(u => {
        const li = document.createElement("li");
        li.textContent = `ID: [${String(u.id).padStart(3,"0")}] - ${u.first_name} ${u.last_name}, login: ${u.login}`;
        li.dataset.id = u.id;
        li.addEventListener("click", () => onUserSelected(u));
        userList.appendChild(li);
      });
    }

    function onUserSelected(user) {
      selectedUserId = user.id;
      summary.textContent = `Wybrano użytkownika: ${user.first_name} ${user.last_name} (login: ${user.login})`;
      summary.style.display = "block";
      deleteBtn.style.display = "inline-block";
      cancelBtn.style.display = "inline-block";
      showBtn.style.display = "none";
    }

    function resetSummary() {
      selectedUserId = null;
      summary.style.display = "none";
      deleteBtn.style.display = "none";
      cancelBtn.style.display = "none";
      showBtn.style.display = "inline-block";
    }

    showBtn.addEventListener("click", populateUsers);
    cancelBtn.addEventListener("click", resetSummary);
    deleteBtn.addEventListener("click", () => {
      if (selectedUserId) {
        alert(`Usunięto użytkownika ID: ${selectedUserId}`);
        resetSummary();
      }
    });
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(TEMPLATE)

if __name__ == "__main__":
    app.run(debug=True)
