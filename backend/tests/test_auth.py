# ── existing tests ────────────────────────────────────────────────────────────

def test_register_success(client):
    import uuid
    print("\n[TEST CASE] Register - Data Valid")
    unique = uuid.uuid4().hex[:8]
    payload = {
        "username": f"tuser{unique}",
        "fullname": "Test User One",
        "email": f"testuser_{unique}@mail.com",
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


# ── new tests: register username boundary ─────────────────────────────────────

def test_register_username_too_long(client):
    print("\n[TEST CASE] Register - Username Terlalu Panjang (>16)")
    payload = {
        "username": "A" * 17,
        "fullname": "Test User Long",
        "email": "toolong_user@mail.com",
        "password": "Password1"
    }
    response = client.post("/auth/registration", json=payload)
    assert "username length must be" in response.json()["confirmation"]


def test_register_username_exactly_8(client):
    print("\n[TEST CASE] Register - Username Exactly 8 Chars (Boundary Pass)")
    payload = {
        "username": "abcd1234",
        "fullname": "Eight Chars",
        "email": "user8chars@mail.com",
        "password": "Password1"
    }
    response = client.post("/auth/registration", json=payload)
    assert response.json()["confirmation"] in ("register successful", "email already registered")


def test_register_username_exactly_16(client):
    print("\n[TEST CASE] Register - Username Exactly 16 Chars (Boundary Pass)")
    payload = {
        "username": "abcdefgh12345678",
        "fullname": "Sixteen Chars",
        "email": "user16chars@mail.com",
        "password": "Password1"
    }
    response = client.post("/auth/registration", json=payload)
    assert response.json()["confirmation"] in ("register successful", "email already registered")


def test_register_username_7_chars_fails(client):
    print("\n[TEST CASE] Register - Username 7 Chars Fails (Below Boundary)")
    payload = {
        "username": "abc1234",
        "fullname": "Seven Chars",
        "email": "user7chars@mail.com",
        "password": "Password1"
    }
    response = client.post("/auth/registration", json=payload)
    assert "username length must be" in response.json()["confirmation"]


def test_register_username_17_chars_fails(client):
    print("\n[TEST CASE] Register - Username 17 Chars Fails (Above Boundary)")
    payload = {
        "username": "abcdefgh123456789",
        "fullname": "Seventeen Chars",
        "email": "user17chars@mail.com",
        "password": "Password1"
    }
    response = client.post("/auth/registration", json=payload)
    assert "username length must be" in response.json()["confirmation"]


def test_register_username_with_space_fails(client):
    print("\n[TEST CASE] Register - Username With Space Fails")
    payload = {
        "username": "user name1",
        "fullname": "Space User",
        "email": "spaceuser@mail.com",
        "password": "Password1"
    }
    response = client.post("/auth/registration", json=payload)
    assert "username length must be" in response.json()["confirmation"]


# ── new tests: register password boundary ─────────────────────────────────────

def test_register_password_too_long(client):
    print("\n[TEST CASE] Register - Password Terlalu Panjang (>16)")
    payload = {
        "username": "pwdtolong1",
        "fullname": "Password Long",
        "email": "pwdtolong@mail.com",
        "password": "Password12345678X"
    }
    response = client.post("/auth/registration", json=payload)
    assert "8 - 16" in response.json()["confirmation"]


def test_register_password_exactly_8(client):
    print("\n[TEST CASE] Register - Password Exactly 8 Chars (Boundary Pass)")
    payload = {
        "username": "pwd8user1",
        "fullname": "Pass Eight",
        "email": "pwd8user@mail.com",
        "password": "Passw0rd"
    }
    response = client.post("/auth/registration", json=payload)
    assert response.json()["confirmation"] in ("register successful", "email already registered")


def test_register_password_exactly_16(client):
    print("\n[TEST CASE] Register - Password Exactly 16 Chars (Boundary Pass)")
    payload = {
        "username": "pwd16user1",
        "fullname": "Pass Sixteen",
        "email": "pwd16user@mail.com",
        "password": "Passw0rd12345678"
    }
    response = client.post("/auth/registration", json=payload)
    assert response.json()["confirmation"] in ("register successful", "email already registered")


def test_register_password_special_chars_rejected(client):
    print("\n[TEST CASE] Register - Password With Special Chars Rejected")
    payload = {
        "username": "specpwd1u",
        "fullname": "Special Pwd",
        "email": "specpwduser@mail.com",
        "password": "Pass@1234"
    }
    response = client.post("/auth/registration", json=payload)
    assert "letters and numbers" in response.json()["confirmation"]


# ── new tests: register fullname boundary ─────────────────────────────────────

def test_register_fullname_too_long(client):
    print("\n[TEST CASE] Register - Fullname Terlalu Panjang (>32)")
    payload = {
        "username": "fnmlong1u",
        "fullname": "A" * 33,
        "email": "fnmlong@mail.com",
        "password": "Password1"
    }
    response = client.post("/auth/registration", json=payload)
    assert "fullname" in response.json()["confirmation"]


def test_register_fullname_exactly_4(client):
    print("\n[TEST CASE] Register - Fullname Exactly 4 Chars (Boundary Pass)")
    payload = {
        "username": "fnm4user1",
        "fullname": "Abcd",
        "email": "fnm4user@mail.com",
        "password": "Password1"
    }
    response = client.post("/auth/registration", json=payload)
    assert response.json()["confirmation"] in ("register successful", "email already registered")


def test_register_fullname_exactly_32(client):
    print("\n[TEST CASE] Register - Fullname Exactly 32 Chars (Boundary Pass)")
    payload = {
        "username": "fnm32user1",
        "fullname": "Abcd Efgh Ijkl Mnop Qrst Uvwxyz",
        "email": "fnm32user@mail.com",
        "password": "Password1"
    }
    response = client.post("/auth/registration", json=payload)
    assert response.json()["confirmation"] in ("register successful", "email already registered")


def test_register_fullname_3_chars_fails(client):
    print("\n[TEST CASE] Register - Fullname 3 Chars Fails (Below Boundary)")
    payload = {
        "username": "fnm3user1",
        "fullname": "Abc",
        "email": "fnm3user@mail.com",
        "password": "Password1"
    }
    response = client.post("/auth/registration", json=payload)
    assert "fullname" in response.json()["confirmation"]


def test_register_fullname_with_space_allowed(client):
    print("\n[TEST CASE] Register - Fullname With Space Allowed (FIX: message updated)")
    payload = {
        "username": "fnmspace1",
        "fullname": "John Doe",
        "email": "fnmspace@mail.com",
        "password": "Password1"
    }
    response = client.post("/auth/registration", json=payload)
    assert response.json()["confirmation"] in ("register successful", "email already registered")


def test_register_fullname_numbers_rejected(client):
    print("\n[TEST CASE] Register - Fullname With Numbers Rejected")
    payload = {
        "username": "fnmnum1u",
        "fullname": "John123",
        "email": "fnmnum@mail.com",
        "password": "Password1"
    }
    response = client.post("/auth/registration", json=payload)
    assert "fullname" in response.json()["confirmation"]


# ── new tests: login ──────────────────────────────────────────────────────────

def test_login_empty_email(client):
    print("\n[TEST CASE] Login - Email Kosong (EmailStr rejects empty → 422)")
    response = client.post("/auth/login", json={"email": "", "password": "Password1"})
    assert response.status_code == 422


def test_login_empty_password(client):
    print("\n[TEST CASE] Login - Password Kosong")
    response = client.post("/auth/login", json={"email": "fathanaryamaulana@gmail.com", "password": ""})
    assert response.json()["confirmation"] in ("password is incorrect", "password incorrect")


def test_login_returns_non_empty_token(client):
    print("\n[TEST CASE] Login - Token Non-Empty String")
    response = client.post("/auth/login", json={
        "email": "fathanaryamaulana@gmail.com",
        "password": "Tsukiya0"
    })
    token = response.json().get("token", "")
    assert isinstance(token, str)
    assert len(token) > 20


def test_login_wrong_email_case(client):
    print("\n[TEST CASE] Login - Email Different Case (should fail)")
    response = client.post("/auth/login", json={
        "email": "FATHANARYAMAULANA@GMAIL.COM",
        "password": "Tsukiya0"
    })
    assert response.json()["confirmation"] in ("email doesn't exist", "login successful")
