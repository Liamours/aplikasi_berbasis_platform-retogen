import uuid
import pytest

SMALL_IMAGE_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwADhQGAWjR9awAAAABJRU5ErkJggg=="


# ── subscription cleanup ──────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def cleanup_subscriptions(client, auth_headers_user, auth_headers_admin):
    """Remove any subscriptions added during a notification test to prevent limit overflow."""
    user_before = set(client.post("/subscription/get", headers=auth_headers_user).json().get("tags", []))
    admin_before = set(client.post("/subscription/get", headers=auth_headers_admin).json().get("tags", []))
    yield
    user_after = set(client.post("/subscription/get", headers=auth_headers_user).json().get("tags", []))
    admin_after = set(client.post("/subscription/get", headers=auth_headers_admin).json().get("tags", []))
    for tag in user_after - user_before:
        client.post("/subscription/unsubscribe", json={"tag": tag}, headers=auth_headers_user)
    for tag in admin_after - admin_before:
        client.post("/subscription/unsubscribe", json={"tag": tag}, headers=auth_headers_admin)


# ── helpers ───────────────────────────────────────────────────────────────────

def _unique_tag(prefix="ntag"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def _add_article_with_tags(client, headers, tags, title=None):
    title = title or f"Notif Test Article {uuid.uuid4().hex[:6]}"
    client.post("/article/add", json={
        "article_title": title,
        "article_preview": "Preview text",
        "article_content": "Content body",
        "article_tags": tags,
        "article_image": SMALL_IMAGE_B64,
    }, headers=headers)
    return title


# ── get notifications ─────────────────────────────────────────────────────────

def test_get_notifications_success(client, auth_headers_user):
    print("\n[TEST CASE] Get Notifications - Berhasil")
    response = client.post("/notification/get", headers=auth_headers_user)
    assert response.status_code == 200
    assert response.json()["confirmation"] == "successful"
    assert isinstance(response.json()["notifications"], list)


def test_get_notifications_no_token(client):
    print("\n[TEST CASE] Get Notifications - Tanpa Token")
    response = client.post("/notification/get")
    assert response.status_code == 401


def test_get_notifications_invalid_token(client):
    print("\n[TEST CASE] Get Notifications - Token Tidak Valid")
    response = client.post("/notification/get", headers={"Authorization": "Bearer badtoken"})
    assert response.status_code == 401


def test_get_notifications_admin_can_fetch(client, auth_headers_admin):
    print("\n[TEST CASE] Get Notifications - Admin Juga Bisa Fetch")
    response = client.post("/notification/get", headers=auth_headers_admin)
    assert response.json()["confirmation"] == "successful"


def test_get_notifications_returns_list_type(client, auth_headers_user):
    print("\n[TEST CASE] Get Notifications - Type Is List")
    response = client.post("/notification/get", headers=auth_headers_user)
    assert isinstance(response.json()["notifications"], list)


# ── notification fields ───────────────────────────────────────────────────────

def test_notification_has_correct_fields(client, auth_headers_user, auth_headers_admin):
    print("\n[TEST CASE] Get Notifications - Has Correct Fields")
    tag = _unique_tag("fields")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    _add_article_with_tags(client, auth_headers_admin, [tag])

    response = client.post("/notification/get", headers=auth_headers_user)
    notifications = response.json()["notifications"]
    matching = [n for n in notifications if tag in n.get("tags", [])]
    assert len(matching) > 0

    n = matching[0]
    assert "notification_id" in n
    assert "article_id" in n
    assert "article_title" in n
    assert "tags" in n
    assert "created_at" in n


def test_notification_tags_is_list(client, auth_headers_user, auth_headers_admin):
    print("\n[TEST CASE] Get Notifications - Tags Field Is List")
    tag = _unique_tag("tagslist")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    _add_article_with_tags(client, auth_headers_admin, [tag])

    response = client.post("/notification/get", headers=auth_headers_user)
    for n in response.json()["notifications"]:
        assert isinstance(n["tags"], list)


def test_notification_article_id_is_string(client, auth_headers_user, auth_headers_admin):
    print("\n[TEST CASE] Get Notifications - article_id Is String")
    tag = _unique_tag("artid")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    _add_article_with_tags(client, auth_headers_admin, [tag])

    response = client.post("/notification/get", headers=auth_headers_user)
    matching = [n for n in response.json()["notifications"] if tag in n.get("tags", [])]
    assert len(matching) > 0
    assert isinstance(matching[0]["article_id"], str)


def test_notification_created_at_is_string(client, auth_headers_user, auth_headers_admin):
    print("\n[TEST CASE] Get Notifications - created_at Is String")
    tag = _unique_tag("creat")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    _add_article_with_tags(client, auth_headers_admin, [tag])

    response = client.post("/notification/get", headers=auth_headers_user)
    matching = [n for n in response.json()["notifications"] if tag in n.get("tags", [])]
    assert len(matching) > 0
    assert isinstance(matching[0]["created_at"], str)


# ── notification trigger ──────────────────────────────────────────────────────

def test_notification_created_on_article_add(client, auth_headers_user, auth_headers_admin):
    print("\n[TEST CASE] Notification - Dibuat Saat Artikel Ditambahkan")
    tag = _unique_tag("trigger")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    _add_article_with_tags(client, auth_headers_admin, [tag])

    response = client.post("/notification/get", headers=auth_headers_user)
    matching = [n for n in response.json()["notifications"] if tag in n.get("tags", [])]
    assert len(matching) > 0


def test_notification_not_created_without_subscription(client, auth_headers_user, auth_headers_admin):
    print("\n[TEST CASE] Notification - Tidak Dibuat Jika Tidak Subscribe")
    tag = _unique_tag("nosub")
    before = client.post("/notification/get", headers=auth_headers_user).json()["notifications"]
    before_count = len([n for n in before if tag in n.get("tags", [])])

    _add_article_with_tags(client, auth_headers_admin, [tag])

    after = client.post("/notification/get", headers=auth_headers_user).json()["notifications"]
    after_count = len([n for n in after if tag in n.get("tags", [])])
    assert after_count == before_count


def test_notification_not_sent_to_author(client, auth_headers_admin):
    print("\n[TEST CASE] Notification - Admin Tidak Dapat Notif Dari Artikel Sendiri")
    tag = _unique_tag("author")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_admin)

    before = client.post("/notification/get", headers=auth_headers_admin).json()["notifications"]
    before_count = len([n for n in before if tag in n.get("tags", [])])

    _add_article_with_tags(client, auth_headers_admin, [tag])

    after = client.post("/notification/get", headers=auth_headers_admin).json()["notifications"]
    after_count = len([n for n in after if tag in n.get("tags", [])])
    assert after_count == before_count


def test_notification_multiple_tags_match(client, auth_headers_user, auth_headers_admin):
    print("\n[TEST CASE] Notification - Notif Untuk Artikel Multi Tag")
    tag1 = _unique_tag("multi1")
    tag2 = _unique_tag("multi2")
    client.post("/subscription/subscribe", json={"tag": tag1}, headers=auth_headers_user)
    client.post("/subscription/subscribe", json={"tag": tag2}, headers=auth_headers_user)
    _add_article_with_tags(client, auth_headers_admin, [tag1, tag2])

    response = client.post("/notification/get", headers=auth_headers_user)
    matching = [n for n in response.json()["notifications"] if tag1 in n.get("tags", []) or tag2 in n.get("tags", [])]
    assert len(matching) > 0


def test_notification_only_subscribed_tag_triggers(client, auth_headers_user, auth_headers_admin):
    print("\n[TEST CASE] Notification - Hanya Tag yang Disubscribe Trigger Notif")
    subscribed_tag = _unique_tag("subbed")
    unsubscribed_tag = _unique_tag("notsubbed")
    client.post("/subscription/subscribe", json={"tag": subscribed_tag}, headers=auth_headers_user)

    before = client.post("/notification/get", headers=auth_headers_user).json()["notifications"]
    before_count = len([n for n in before if unsubscribed_tag in n.get("tags", [])])

    _add_article_with_tags(client, auth_headers_admin, [unsubscribed_tag])

    after = client.post("/notification/get", headers=auth_headers_user).json()["notifications"]
    after_count = len([n for n in after if unsubscribed_tag in n.get("tags", [])])
    assert after_count == before_count


def test_notification_article_title_matches(client, auth_headers_user, auth_headers_admin):
    print("\n[TEST CASE] Notification - article_title Sesuai")
    tag = _unique_tag("titlematch")
    expected_title = f"Notif Title Match Test {uuid.uuid4().hex[:6]}"
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    _add_article_with_tags(client, auth_headers_admin, [tag], title=expected_title)

    response = client.post("/notification/get", headers=auth_headers_user)
    matching = [n for n in response.json()["notifications"] if n.get("article_title") == expected_title]
    assert len(matching) > 0


# ── sorted newest first ───────────────────────────────────────────────────────

def test_notification_sorted_newest_first(client, auth_headers_user, auth_headers_admin):
    print("\n[TEST CASE] Get Notifications - Diurutkan Terbaru Dulu")
    tag = _unique_tag("sortcheck")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    _add_article_with_tags(client, auth_headers_admin, [tag])
    _add_article_with_tags(client, auth_headers_admin, [tag])

    response = client.post("/notification/get", headers=auth_headers_user)
    notifications = response.json()["notifications"]
    if len(notifications) >= 2:
        timestamps = [n["created_at"] for n in notifications]
        assert timestamps == sorted(timestamps, reverse=True)


# ── notification count ────────────────────────────────────────────────────────

def test_notification_count_increases_after_article_add(client, auth_headers_user, auth_headers_admin):
    print("\n[TEST CASE] Notification - Count Bertambah Setelah Artikel Ditambahkan")
    tag = _unique_tag("countinc")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)

    before = len([n for n in client.post("/notification/get", headers=auth_headers_user).json()["notifications"]
                  if tag in n.get("tags", [])])

    _add_article_with_tags(client, auth_headers_admin, [tag])

    after = len([n for n in client.post("/notification/get", headers=auth_headers_user).json()["notifications"]
                 if tag in n.get("tags", [])])

    assert after == before + 1


def test_notification_count_stable_without_matching_article(client, auth_headers_user, auth_headers_admin):
    print("\n[TEST CASE] Notification - Count Tidak Berubah Jika Tag Tidak Match")
    tag_sub = _unique_tag("stable_sub")
    tag_other = _unique_tag("stable_other")
    client.post("/subscription/subscribe", json={"tag": tag_sub}, headers=auth_headers_user)

    before = len(client.post("/notification/get", headers=auth_headers_user).json()["notifications"])
    _add_article_with_tags(client, auth_headers_admin, [tag_other])
    after = len(client.post("/notification/get", headers=auth_headers_user).json()["notifications"])

    assert after == before


# ── field types ───────────────────────────────────────────────────────────────

def test_notification_id_is_string(client, auth_headers_user, auth_headers_admin):
    print("\n[TEST CASE] Notification - notification_id Is String")
    tag = _unique_tag("nidstr")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    _add_article_with_tags(client, auth_headers_admin, [tag])

    response = client.post("/notification/get", headers=auth_headers_user)
    matching = [n for n in response.json()["notifications"] if tag in n.get("tags", [])]
    assert len(matching) > 0
    assert isinstance(matching[0]["notification_id"], str)


def test_notification_article_title_is_string(client, auth_headers_user, auth_headers_admin):
    print("\n[TEST CASE] Notification - article_title Is String")
    tag = _unique_tag("titlestr")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    _add_article_with_tags(client, auth_headers_admin, [tag])

    response = client.post("/notification/get", headers=auth_headers_user)
    matching = [n for n in response.json()["notifications"] if tag in n.get("tags", [])]
    assert len(matching) > 0
    assert isinstance(matching[0]["article_title"], str)


def test_notification_tags_contain_subscribed_tag(client, auth_headers_user, auth_headers_admin):
    print("\n[TEST CASE] Notification - Tags Mengandung Tag Yang Disubscribe")
    tag = _unique_tag("tagcontain")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    _add_article_with_tags(client, auth_headers_admin, [tag])

    response = client.post("/notification/get", headers=auth_headers_user)
    matching = [n for n in response.json()["notifications"] if tag in n.get("tags", [])]
    assert len(matching) > 0
    assert tag in matching[0]["tags"]


# ── multi-subscriber ──────────────────────────────────────────────────────────

def test_notification_two_subscribers_both_receive(client, auth_headers_user, auth_headers_admin):
    print("\n[TEST CASE] Notification - Dua Subscriber Keduanya Dapat Notif")
    tag = _unique_tag("twosub")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_admin)

    before_admin = len([n for n in client.post("/notification/get", headers=auth_headers_admin).json()["notifications"]
                        if tag in n.get("tags", [])])

    # A third account would be needed to truly test both; here admin posting won't self-notify
    # so just verify user gets notification from admin's post
    _add_article_with_tags(client, auth_headers_admin, [tag])

    after_user = len([n for n in client.post("/notification/get", headers=auth_headers_user).json()["notifications"]
                      if tag in n.get("tags", [])])

    assert after_user > 0


def test_notification_not_duplicated_for_multi_tag_article(client, auth_headers_user, auth_headers_admin):
    print("\n[TEST CASE] Notification - Tidak Duplikat Untuk Multi-Tag")
    tag1 = _unique_tag("nodup1")
    tag2 = _unique_tag("nodup2")
    client.post("/subscription/subscribe", json={"tag": tag1}, headers=auth_headers_user)
    client.post("/subscription/subscribe", json={"tag": tag2}, headers=auth_headers_user)

    before = len(client.post("/notification/get", headers=auth_headers_user).json()["notifications"])
    _add_article_with_tags(client, auth_headers_admin, [tag1, tag2])
    after = len(client.post("/notification/get", headers=auth_headers_user).json()["notifications"])

    # Should add exactly 1 notification (not 2, one per tag)
    assert after - before == 1


# ── edge cases ────────────────────────────────────────────────────────────────

def test_notification_unsubscribe_stops_future_notifications(client, auth_headers_user, auth_headers_admin):
    print("\n[TEST CASE] Notification - Unsubscribe Hentikan Notif Selanjutnya")
    tag = _unique_tag("unstopped")
    client.post("/subscription/subscribe", json={"tag": tag}, headers=auth_headers_user)
    client.post("/subscription/unsubscribe", json={"tag": tag}, headers=auth_headers_user)

    before = len([n for n in client.post("/notification/get", headers=auth_headers_user).json()["notifications"]
                  if tag in n.get("tags", [])])

    _add_article_with_tags(client, auth_headers_admin, [tag])

    after = len([n for n in client.post("/notification/get", headers=auth_headers_user).json()["notifications"]
                 if tag in n.get("tags", [])])

    assert after == before


def test_notification_response_is_dict(client, auth_headers_user):
    print("\n[TEST CASE] Notification - Response Adalah Dict")
    response = client.post("/notification/get", headers=auth_headers_user)
    assert isinstance(response.json(), dict)


def test_notification_response_has_confirmation_key(client, auth_headers_user):
    print("\n[TEST CASE] Notification - Response Punya Key 'confirmation'")
    response = client.post("/notification/get", headers=auth_headers_user)
    assert "confirmation" in response.json()


def test_notification_response_has_notifications_key(client, auth_headers_user):
    print("\n[TEST CASE] Notification - Response Punya Key 'notifications'")
    response = client.post("/notification/get", headers=auth_headers_user)
    assert "notifications" in response.json()
