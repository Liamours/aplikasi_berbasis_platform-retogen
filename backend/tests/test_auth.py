def test_register_success(client):
    print("\n[TEST CASE] Register - Data Valid")
    payload = {
        "username": "testuser1",
        "fullname": "Test User One",
        "email": "testuser1@mail.com",
        "password": "Password1"
    }
    response = client.post("/auth/registration", json=payload)
    print(f"    response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["confirmation"] == "register successful"


def test_register_invalid_username_too_short(client):
    print("\n[TEST CASE] Register - Username Terlalu Pendek")
    payload = {
        "username": "raf",
        "fullname": "Rafiq Labib",
        "email": "raf@mail.com",
        "password": "Password1"
    }
    response = client.post("/auth/registration", json=payload)
    print(f"    response: {response.json()}")
    assert "username length must be" in response.json()["confirmation"]


def test_register_invalid_username_special_chars(client):
    print("\n[TEST CASE] Register - Username Mengandung Karakter Spesial")
    payload = {
        "username": "rafiq!@#",
        "fullname": "Rafiq Labib",
        "email": "rafiqspec@mail.com",
        "password": "Password1"
    }
    response = client.post("/auth/registration", json=payload)
    print(f"    response: {response.json()}")
    assert "username length must be" in response.json()["confirmation"]


def test_register_duplicate_email(client):
    print("\n[TEST CASE] Register - Email Duplikat")
    payload = {
        "username": "dupuser1",
        "fullname": "Dup User",
        "email": "dupuser@mail.com",
        "password": "Password1"
    }
    client.post("/auth/registration", json=payload)
    payload["username"] = "dupuser2"
    response = client.post("/auth/registration", json=payload)
    print(f"    response: {response.json()}")
    assert response.json()["confirmation"] == "email already registered"


def test_register_password_no_uppercase(client):
    print("\n[TEST CASE] Register - Password Tanpa Huruf Besar")
    payload = {
        "username": "testuser2",
        "fullname": "Test User Two",
        "email": "testuser2@mail.com",
        "password": "password1"
    }
    response = client.post("/auth/registration", json=payload)
    print(f"    response: {response.json()}")
    assert "uppercase" in response.json()["confirmation"]


def test_register_password_no_lowercase(client):
    print("\n[TEST CASE] Register - Password Tanpa Huruf Kecil")
    payload = {
        "username": "testuser3",
        "fullname": "Test User Three",
        "email": "testuser3@mail.com",
        "password": "PASSWORD1"
    }
    response = client.post("/auth/registration", json=payload)
    print(f"    response: {response.json()}")
    assert "lowercase" in response.json()["confirmation"]


def test_register_password_no_number(client):
    print("\n[TEST CASE] Register - Password Tanpa Angka")
    payload = {
        "username": "testuser4",
        "fullname": "Test User Four",
        "email": "testuser4@mail.com",
        "password": "Password"
    }
    response = client.post("/auth/registration", json=payload)
    print(f"    response: {response.json()}")
    assert "number" in response.json()["confirmation"]


def test_register_password_only_numbers(client):
    print("\n[TEST CASE] Register - Password Hanya Angka")
    payload = {
        "username": "testuser5",
        "fullname": "Test User Five",
        "email": "testuser5@mail.com",
        "password": "12345678"
    }
    response = client.post("/auth/registration", json=payload)
    print(f"    response: {response.json()}")
    assert response.status_code == 200
    assert "uppercase" in response.json()["confirmation"] or "lowercase" in response.json()["confirmation"]


def test_register_password_too_short(client):
    print("\n[TEST CASE] Register - Password Terlalu Pendek")
    payload = {
        "username": "testuser6",
        "fullname": "Test User Six",
        "email": "testuser6@mail.com",
        "password": "Pass1"
    }
    response = client.post("/auth/registration", json=payload)
    print(f"    response: {response.json()}")
    assert "8 - 16" in response.json()["confirmation"]


def test_register_fullname_too_short(client):
    print("\n[TEST CASE] Register - Fullname Terlalu Pendek")
    payload = {
        "username": "testuser7",
        "fullname": "Ab",
        "email": "testuser7@mail.com",
        "password": "Password1"
    }
    response = client.post("/auth/registration", json=payload)
    print(f"    response: {response.json()}")
    assert "fullname" in response.json()["confirmation"]


def test_login_success(client):
    print("\n[TEST CASE] Login - Berhasil")
    response = client.post("/auth/login", json={
        "email": "fathanaryamaulana@gmail.com",
        "password": "Tsukiya0"
    })
    print(f"    response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["confirmation"] == "login successful"
    assert "token" in response.json()


def test_login_wrong_password(client):
    print("\n[TEST CASE] Login - Password Salah")
    response = client.post("/auth/login", json={
        "email": "fathanaryamaulana@gmail.com",
        "password": "WrongPass0"
    })
    print(f"    response: {response.json()}")
    assert response.json()["confirmation"] == "password incorrect"


def test_login_email_not_found(client):
    print("\n[TEST CASE] Login - Email Tidak Ditemukan")
    response = client.post("/auth/login", json={
        "email": "notexist@mail.com",
        "password": "Password1"
    })
    print(f"    response: {response.json()}")
    assert response.json()["confirmation"] == "email doesn't exist"


def test_login_user_role(client):
    print("\n[TEST CASE] Login - User Biasa")
    response = client.post("/auth/login", json={
        "email": "steven098@gmail.com",
        "password": "123Asdfg"
    })
    print(f"    response: {response.json()}")
    assert response.json()["confirmation"] == "login successful"
    assert "token" in response.json()
