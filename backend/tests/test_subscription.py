import uuid
import pytest


# ── module setup ──────────────────────────────────────────────────────────────

@pytest.fixture(scope="module", autouse=True)
def clear_subs_before_module(client, auth_headers_user, auth_headers_admin):
    """Wipe all subscriptions before this module runs (previous runs may fill the limit)."""
    for headers in (auth_headers_user, auth_headers_admin):
        get_resp = client.post("/subscription/get", headers=headers)
        for tag in get_resp.json().get("tags", []):
            client.post("/subscription/unsubscribe", json={"tag": tag}, headers=headers)
    yield


# ── helpers ───────────────────────────────────────────────────────────────────

def _unique_tag(prefix="tag"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


# ── subscribe ─────────────────────────────────────────────────────────────────

def test_subscribe_success(client, auth_headers_user):
    print("\n[TEST CASE] Subscribe - Berhasil")
    tag = _unique_tag("gaming")
    response = client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "subscribed"


def test_subscribe_already_subscribed(client, auth_headers_user):
    print("\n[TEST CASE] Subscribe - Sudah Terdaftar")
    tag = _unique_tag("dup")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    response = client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "already subscribed"


def test_subscribe_empty_tag(client, auth_headers_user):
    print("\n[TEST CASE] Subscribe - Tag Kosong")
    response = client.post("/subscription/subscribe", json={"tag": "   "}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "tag cannot be empty"


def test_subscribe_no_token(client):
    print("\n[TEST CASE] Subscribe - Tanpa Token")
    response = client.post("/subscription/subscribe", json={"tag": "gaming"})
    assert response.status_code == 401


def test_subscribe_invalid_token(client):
    print("\n[TEST CASE] Subscribe - Token Tidak Valid")
    response = client.post("/subscription/subscribe", json={"tag": "gaming"}, headers={"Authorization": "Bearer badtoken"})
    assert response.status_code == 401


def test_subscribe_normalizes_to_lowercase(client, auth_headers_user):
    print("\n[TEST CASE] Subscribe - Tag Dinormalisasi ke Lowercase")
    tag = _unique_tag("UPPER")
    response = client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "subscribed"
    get_resp = client.post("/subscription/get", headers=auth_headers_user)
    assert tag.lower() in get_resp.json()["tags"]


def test_subscribe_whitespace_tag_trimmed(client, auth_headers_user):
    print("\n[TEST CASE] Subscribe - Tag Dengan Spasi Ditriming")
    tag = _unique_tag("trim")
    response = client.post("/subscription/subscribe", json={"tag": f"  {tag}  "}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "subscribed"
    get_resp = client.post("/subscription/get", headers=auth_headers_user)
    assert tag in get_resp.json()["tags"]


def test_subscribe_admin_can_subscribe(client, auth_headers_admin):
    print("\n[TEST CASE] Subscribe - Admin Juga Bisa Subscribe")
    tag = _unique_tag("admintag")
    response = client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "subscribed"


def test_subscribe_multiple_tags(client, auth_headers_user):
    print("\n[TEST CASE] Subscribe - Multiple Tags Berbeda")
    tags = [_unique_tag(f"multi{i}") for i in range(3)]
    for tag in tags:
        r = client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
        assert r.json()["confirmation"] == "subscribed"
    get_resp = client.post("/subscription/get", headers=auth_headers_user)
    for tag in tags:
        assert tag in get_resp.json()["tags"]


def test_subscribe_and_get_reflects_immediately(client, auth_headers_user):
    print("\n[TEST CASE] Subscribe - Get Langsung Menunjukkan Tag Baru")
    tag = _unique_tag("immediate")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    get_resp = client.post("/subscription/get", headers=auth_headers_user)
    assert tag.lower() in get_resp.json()["tags"]


def test_subscribe_count_increments(client, auth_headers_user):
    print("\n[TEST CASE] Subscribe - Count Bertambah Setelah Subscribe")
    before = len(client.post("/subscription/get", headers=auth_headers_user).json()["tags"])
    tag = _unique_tag("countcheck")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    after = len(client.post("/subscription/get", headers=auth_headers_user).json()["tags"])
    assert after == before + 1


def test_subscribe_tag_with_special_chars(client, auth_headers_user):
    print("\n[TEST CASE] Subscribe - Tag Dengan Karakter Khusus")
    tag = _unique_tag("spec!@#")
    response = client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    assert response.json()["confirmation"] in ("subscribed", "tag cannot be empty")


def test_subscribe_very_long_tag(client, auth_headers_user):
    print("\n[TEST CASE] Subscribe - Tag Sangat Panjang")
    tag = "a" * 200
    response = client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    assert "confirmation" in response.json()


# ── unsubscribe ───────────────────────────────────────────────────────────────

def test_unsubscribe_success(client, auth_headers_user):
    print("\n[TEST CASE] Unsubscribe - Berhasil")
    tag = _unique_tag("unsub")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    response = client.post("/subscription/unsubscribe", json={"tag": tag}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "unsubscribed"


def test_unsubscribe_not_subscribed(client, auth_headers_user):
    print("\n[TEST CASE] Unsubscribe - Belum Subscribe")
    response = client.post("/subscription/unsubscribe", json={"tag": "totallynotexist99xyz"}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "not subscribed"


def test_unsubscribe_no_token(client):
    print("\n[TEST CASE] Unsubscribe - Tanpa Token")
    response = client.post("/subscription/unsubscribe", json={"tag": "gaming"})
    assert response.status_code == 401


def test_unsubscribe_removes_tag_from_list(client, auth_headers_user):
    print("\n[TEST CASE] Unsubscribe - Tag Terhapus dari List")
    tag = _unique_tag("removeme")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    client.post("/subscription/unsubscribe", json={"tag": tag}, headers=auth_headers_user)
    get_resp = client.post("/subscription/get", headers=auth_headers_user)
    assert tag not in get_resp.json()["tags"]


def test_unsubscribe_then_resubscribe(client, auth_headers_user):
    print("\n[TEST CASE] Unsubscribe - Bisa Resubscribe Setelah Unsubscribe")
    tag = _unique_tag("resub")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    client.post("/subscription/unsubscribe", json={"tag": tag}, headers=auth_headers_user)
    response = client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "subscribed"


def test_unsubscribe_does_not_affect_other_tags(client, auth_headers_user):
    print("\n[TEST CASE] Unsubscribe - Tidak Hapus Tag Lain")
    tag_keep = _unique_tag("keep")
    tag_remove = _unique_tag("remove")
    client.post("/subscription/subscribe", json={"tag": tag_keep}, headers=auth_headers_user)
    client.post("/subscription/subscribe", json={"tag": tag_remove}, headers=auth_headers_user)
    client.post("/subscription/unsubscribe", json={"tag": tag_remove}, headers=auth_headers_user)
    get_resp = client.post("/subscription/get", headers=auth_headers_user)
    assert tag_keep in get_resp.json()["tags"]
    assert tag_remove not in get_resp.json()["tags"]


def test_unsubscribe_empty_tag(client, auth_headers_user):
    print("\n[TEST CASE] Unsubscribe - Tag Kosong")
    response = client.post("/subscription/unsubscribe", json={"tag": "   "}, headers=auth_headers_user)
    assert response.json()["confirmation"] in ("not subscribed", "tag cannot be empty")


def test_unsubscribe_normalizes_to_lowercase(client, auth_headers_user):
    print("\n[TEST CASE] Unsubscribe - Tag Uppercase Tetap Bisa Unsubscribe")
    tag = _unique_tag("ucaseun")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    response = client.post("/subscription/unsubscribe", json={"tag": tag.upper()}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "unsubscribed"
    get_resp = client.post("/subscription/get", headers=auth_headers_user)
    assert tag.lower() not in get_resp.json()["tags"]


def test_unsubscribe_count_decrements(client, auth_headers_user):
    print("\n[TEST CASE] Unsubscribe - Count Berkurang Setelah Unsubscribe")
    tag = _unique_tag("countdown")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    before = len(client.post("/subscription/get", headers=auth_headers_user).json()["tags"])
    client.post("/subscription/unsubscribe", json={"tag": tag}, headers=auth_headers_user)
    after = len(client.post("/subscription/get", headers=auth_headers_user).json()["tags"])
    assert after == before - 1


def test_unsubscribe_invalid_token(client):
    print("\n[TEST CASE] Unsubscribe - Token Tidak Valid")
    response = client.post("/subscription/unsubscribe", json={"tag": "sometag"}, headers={"Authorization": "Bearer faketoken"})
    assert response.status_code == 401


# ── get subscriptions ─────────────────────────────────────────────────────────

def test_get_subscriptions_success(client, auth_headers_user):
    print("\n[TEST CASE] Get Subscriptions - Berhasil")
    response = client.post("/subscription/get", headers=auth_headers_user)
    assert response.json()["confirmation"] == "successful"
    assert isinstance(response.json()["tags"], list)


def test_get_subscriptions_no_token(client):
    print("\n[TEST CASE] Get Subscriptions - Tanpa Token")
    response = client.post("/subscription/get")
    assert response.status_code == 401


def test_get_subscriptions_contains_subscribed_tag(client, auth_headers_user):
    print("\n[TEST CASE] Get Subscriptions - Berisi Tag yang Disubscribe")
    tag = _unique_tag("verify")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    response = client.post("/subscription/get", headers=auth_headers_user)
    assert tag in response.json()["tags"]


def test_get_subscriptions_returns_list(client, auth_headers_user):
    print("\n[TEST CASE] Get Subscriptions - Returns List Type")
    response = client.post("/subscription/get", headers=auth_headers_user)
    assert isinstance(response.json()["tags"], list)


def test_get_subscriptions_admin_also_gets_list(client, auth_headers_admin):
    print("\n[TEST CASE] Get Subscriptions - Admin Juga Bisa Get")
    response = client.post("/subscription/get", headers=auth_headers_admin)
    assert response.json()["confirmation"] == "successful"
    assert isinstance(response.json()["tags"], list)


def test_get_subscriptions_invalid_token(client):
    print("\n[TEST CASE] Get Subscriptions - Token Tidak Valid")
    response = client.post("/subscription/get", headers={"Authorization": "Bearer faketoken"})
    assert response.status_code == 401


# ── limit ─────────────────────────────────────────────────────────────────────

def test_subscribe_limit_reached_at_21(client, auth_headers_user):
    print("\n[TEST CASE] Subscribe - Limit 20 Tags")
    # clear slate first
    get_resp = client.post("/subscription/get", headers=auth_headers_user)
    for existing_tag in get_resp.json()["tags"]:
        client.post("/subscription/unsubscribe", json={"tag": existing_tag}, headers=auth_headers_user)

    for i in range(20):
        client.post("/subscription/subscribe", json={"tag": f"limittag{i:02d}"}, headers=auth_headers_user)

    response = client.post("/subscription/subscribe", json={"tag": "overflowtagxyz"}, headers=auth_headers_user)
    assert response.json()["confirmation"] == "limit reached"


def test_subscribe_exactly_20_succeeds(client, auth_headers_admin):
    print("\n[TEST CASE] Subscribe - Exactly 20 Tags Should Succeed")
    get_resp = client.post("/subscription/get", headers=auth_headers_admin)
    for existing_tag in get_resp.json()["tags"]:
        client.post("/subscription/unsubscribe", json={"tag": existing_tag}, headers=auth_headers_admin)

    for i in range(19):
        client.post("/subscription/subscribe", json={"tag": f"exacttag{i:02d}"}, headers=auth_headers_admin)

    response = client.post("/subscription/subscribe", json={"tag": "exacttag19"}, headers=auth_headers_admin)
    assert response.json()["confirmation"] == "subscribed"
    get_resp = client.post("/subscription/get", headers=auth_headers_admin)
    assert len(get_resp.json()["tags"]) == 20
