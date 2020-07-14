function authenticateUser(user, password)
{
    var token = user + ":" + password;
    var hash = btoa(token);
    return "Basic " + hash;
}

function CallWebAPI(apiName) {
    if (apiName == "getAllAnimals") {
        var method = "GET"
        var url = "http://127.0.0.1:8000/api/animal/"
        getAllAnimals(method, url)
    }
    if (apiName == "getAnimal") {
        var animalID = document.getElementById("id_animalid")
        var method = "GET"
        var url = "http://127.0.0.1:8000/api/animal/" + animalID.value + "/"
        getAnimal(method, url)
    }
    if (apiName == "postAnimalAdd") {
        var method = "POST"
        var url = "http://127.0.0.1:8000/api/animal/add/"
        postAnimalAdd(method, url)
    }
    if (apiName == "postAnimalEdit") {
        var animalID = document.getElementById("id_animalid_edit").value
        var method = "POST"
        var url = "http://127.0.0.1:8000/api/animal/" + animalID + "/edit/"
        postAnimalEdit(method, url)
    }
    if (apiName == "deleteAnimalDelete") {
        var animalID = document.getElementById("id_animalid_delete").value
        var method = "DELETE"
        var url = "http://127.0.0.1:8000/api/animal/" + animalID + "/delete/"
        deleteAnimalDelete(method, url)
    }
}

function getAllAnimals(method, url) {
    var request = new XMLHttpRequest();
    request.open(method, url, false);
    request.send();
    get_all_animals.innerHTML = "Response Code: " + request.status + "\n" + request.responseText;
}

function getAnimal(method, url) {
    var request = new XMLHttpRequest();
    request.open(method, url, false);
    request.send();
    get_animal.innerHTML = "Response Code: " + request.status + "\n" + request.responseText;
}

function postAnimalAdd(method, url) {
    var userName = document.getElementById("username_add").value
    var passWord = document.getElementById("password_add").value

    var name = document.getElementById("id_name_add").value
    var age = document.getElementById("id_age_add").value
    var arrival_date = document.getElementById("id_arrival_date_add").value
    var weight = document.getElementById("id_weight_add").value
    var height = document.getElementById("id_height_add").value
    var spec_features = document.getElementById("id_spec_features_add").value

    var body = 'name=' + encodeURIComponent(name) +
            '&age=' + encodeURIComponent(age) + '&arrival_date=' + encodeURIComponent(arrival_date) +
            '&weight=' + encodeURIComponent(weight) + '&height=' + encodeURIComponent(height) +
            '&spec_features=' + encodeURIComponent(spec_features);

    var request = new XMLHttpRequest();
    request.open(method, url, false);
    request.setRequestHeader("Authorization", authenticateUser(userName, passWord));
    request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    request.send(body);

    add_animal.innerHTML = "Response Code: " + request.status + "\n" + request.responseText;
}

function postAnimalEdit(method, url) {
    var userName = document.getElementById("username_edit").value
    var passWord = document.getElementById("password_edit").value

    var name = document.getElementById("id_name_edit").value
    var age = document.getElementById("id_age_edit").value
    var arrival_date = document.getElementById("id_arrival_date_edit").value
    var weight = document.getElementById("id_weight_edit").value
    var height = document.getElementById("id_height_edit").value
    var spec_features = document.getElementById("id_spec_features_edit").value

    var body = 'name=' + encodeURIComponent(name) +
            '&age=' + encodeURIComponent(age) + '&arrival_date=' + encodeURIComponent(arrival_date) +
            '&weight=' + encodeURIComponent(weight) + '&height=' + encodeURIComponent(height) +
            '&spec_features=' + encodeURIComponent(spec_features);

    var request = new XMLHttpRequest();
    request.open(method, url, false);
    request.setRequestHeader("Authorization", authenticateUser(userName, passWord));
    request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    request.send(body);

    edit_animal.innerHTML = "Response Code: " + request.status + "\n" + request.responseText;
}

function deleteAnimalDelete(method, url) {
    var userName = document.getElementById("username_delete").value
    var passWord = document.getElementById("password_delete").value

    var request = new XMLHttpRequest();
    request.open(method, url, false);
    request.setRequestHeader("Authorization", authenticateUser(userName, passWord));
    request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    request.send();

    animal_delete.innerHTML = "Response Code: " + request.status + "\n" + request.responseText;
}

  $(function () {
    $('#id_arrival_date').datepicker();
  });

  $(function () {
    $('#id_arrival_date_add').datepicker();
  });

  $(function () {
    $('#id_arrival_date_edit').datepicker();
  });