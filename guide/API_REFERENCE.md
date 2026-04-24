# API Reference

Base URL: `http://localhost:8000`

All protected endpoints require a JWT token in the Authorization header:
`Authorization: Bearer <token>`

All endpoints use POST method and accept/return JSON.

---

## Auth

### POST /auth/registration

No auth required.

Request:
```json
{
  "username": "string",
  "fullname": "string",
  "email": "string",
  "password": "string"
}
```

Rules:
- username: 8–16 chars, alphanumeric only
- fullname: 4–32 chars, letters and spaces only
- password: 8–16 chars, must contain uppercase, lowercase, and number

Response:
```json
{ "confirmation": "register successful" }
```

Possible confirmation values: `register successful`, `email already registered`, or a validation message describing which field failed.

---

### POST /auth/login

No auth required.

Request:
```json
{
  "email": "string",
  "password": "string"
}
```

Response:
```json
{
  "confirmation": "login successful",
  "token": "string"
}
```

Possible confirmation values: `login successful`, `email doesn't exist`, `password incorrect`.

---

## Article

### POST /article/main_page

Auth required.

Request:
```json
{
  "sort": "string",
  "tag": "string",
  "search": "string"
}
```

All fields are optional. `sort` accepted values: `newest` (default), `oldest`, `highest_rated`, `most_commented`, `most_reported`, `by_tag`, `search_title`. When `sort` is `by_tag`, provide `tag`. When `sort` is `search_title`, provide `search`.

Response:
```json
{
  "confirmation": "fetch data successful",
  "username": "string",
  "sort": "string",
  "tag": "string",
  "search": "string",
  "list_article": [
    {
      "article_id": "string",
      "article_title": "string",
      "article_preview": "string",
      "article_tags": ["string"],
      "article_image": "base64 string or null"
    }
  ]
}
```

---

### POST /article/view

Auth required.

Request:
```json
{ "article_id": "string" }
```

Response:
```json
{
  "confirmation": "successful",
  "userclass": "user or admin",
  "user_email": "string",
  "username": "string",
  "article_title": "string",
  "article_content": "string",
  "article_tags": ["string"],
  "article_image": "base64 string or null",
  "comments": [
    {
      "comment_id": "string",
      "parent_comment_id": "string or null",
      "owner": "string",
      "user_email": "string",
      "comment_content": "string"
    }
  ],
  "ratings": [
    {
      "rating_id": "string",
      "owner": "string",
      "user_email": "string",
      "rating_value": 1
    }
  ],
  "reports": [
    {
      "report_id": "string",
      "description": "string",
      "created_at": "string"
    }
  ]
}
```

`reports` field is only present when the requester is admin.

---

### POST /article/add

Auth required. Admin only.

Request:
```json
{
  "article_title": "string",
  "article_preview": "string",
  "article_content": "string",
  "article_tags": ["string"],
  "article_image": "base64 string"
}
```

Rules:
- title: 1–256 chars
- preview: 1–128 chars
- content: 1–65536 chars
- tags: at least one required, stored lowercase and trimmed
- image: must be valid base64-encoded PNG or JPEG

Response:
```json
{ "confirmation": "success: article added" }
```

---

### POST /article/edit/get

Auth required. Admin only.

Request:
```json
{ "article_id": "string" }
```

Response:
```json
{
  "confirmation": "successful",
  "article_id": "string",
  "article_title": "string",
  "article_preview": "string",
  "article_content": "string",
  "article_tags": ["string"],
  "article_image": "base64 string or null"
}
```

---

### POST /article/edit/update

Auth required. Admin only.

Request:
```json
{
  "article_id": "string",
  "article_title": "string",
  "article_preview": "string",
  "article_content": "string",
  "article_tags": ["string"],
  "article_image": "base64 string"
}
```

Same validation rules as `/article/add`.

Response:
```json
{ "confirmation": "successful: article edited" }
```

---

### POST /article/delete

Auth required. Admin only.

Request:
```json
{ "article_id": "string" }
```

Response:
```json
{ "confirmation": "successful: article deleted" }
```

---

### POST /article/verification

Auth required. Admin only. No request body.

Response:
```json
{ "confirmation": "successful" }
```

---

## Comment

### POST /comment/add

Auth required.

Request:
```json
{
  "article_id": "string",
  "comment_content": "string",
  "parent_comment_id": "string or null"
}
```

Rules:
- comment_content: 1–8192 chars
- parent_comment_id: omit or set null for root comment, provide a valid comment_id for a reply

Response returns the full updated article view (same shape as `/article/view` response, plus `confirmation`).

---

### POST /comment/edit/get

Auth required. Owner only.

Request:
```json
{ "comment_id": "string" }
```

Response:
```json
{
  "confirmation": "successful",
  "comment_id": "string",
  "article_id": "string",
  "user_email": "string",
  "parent_comment_id": "string or null",
  "comment_content": "string",
  "owner": "string"
}
```

---

### POST /comment/edit/update

Auth required. Owner only.

Request:
```json
{
  "comment_id": "string",
  "article_id": "string",
  "comment_content": "string",
  "parent_comment_id": "string or null"
}
```

Rules:
- comment_content: 1–8192 chars

Response returns the full updated article view (same shape as `/article/view` response, plus `confirmation`).

---

### POST /comment/delete

Auth required. Owner or admin.

Request:
```json
{ "comment_id": "string" }
```

Response returns the full updated article view (same shape as `/article/view` response, plus `confirmation`).

---

## Rating

### POST /rating/add

Auth required. One rating per user per article.

Request:
```json
{
  "article_id": "string",
  "rating_value": 1
}
```

Rules:
- rating_value: integer 1–5

Response returns the full updated article view (same shape as `/article/view` response, plus `confirmation`). Confirmation is `already rated` if the user already rated this article.

---

### POST /rating/edit/get

Auth required. Owner only.

Request:
```json
{
  "article_id": "string",
  "rating_id": "string"
}
```

Response:
```json
{
  "confirmation": "successful",
  "rating": {
    "rating_id": "string",
    "article_id": "string",
    "owner_id": "string",
    "user_email": "string",
    "rating_value": 1,
    "created_at": "string"
  }
}
```

---

### POST /rating/edit/update

Auth required. Owner only.

Request:
```json
{
  "rating_id": "string",
  "article_id": "string",
  "rating_value": 1
}
```

Rules:
- rating_value: integer 1–5

Response returns the full updated article view (same shape as `/article/view` response, plus `confirmation`).

---

## Report

### POST /report_article/add

Auth required.

Request:
```json
{
  "article_id": "string",
  "description": "string"
}
```

Rules:
- description must not be empty or whitespace only

Response:
```json
{ "confirmation": "successful: article reported" }
```

Possible confirmation values: `successful: article reported`, `please fill description`, `invalid article_id`.

---

### POST /report_user/report_user

Auth required.

Request:
```json
{
  "reported_user_email": "string",
  "description": "string"
}
```

Rules:
- Cannot report yourself
- reported_user_email must exist

Response:
```json
{ "confirmation": "successful: user reported" }
```

Possible confirmation values: `successful: user reported`, `cannot report self`, `user not found`.

---

### POST /report_user/get_user_profile

Auth required.

Request:
```json
{ "user_email": "string" }
```

Response:
```json
{
  "confirmation": "successful",
  "user": {
    "user_email": "string",
    "username": "string",
    "fullname": "string",
    "role": "string",
    "created_at": "string"
  }
}
```

---

## Subscription

### POST /subscription/subscribe

Auth required.

Request:
```json
{ "tag": "string" }
```

Tag is automatically trimmed and lowercased before storage.

Response:
```json
{ "confirmation": "subscribed" }
```

Possible confirmation values: `subscribed`, `already subscribed`, `limit reached`, `tag cannot be empty`.

---

### POST /subscription/unsubscribe

Auth required.

Request:
```json
{ "tag": "string" }
```

Response:
```json
{ "confirmation": "unsubscribed" }
```

Possible confirmation values: `unsubscribed`, `not subscribed`, `tag cannot be empty`.

---

### POST /subscription/get

Auth required. No request body.

Response:
```json
{
  "confirmation": "successful",
  "tags": ["string"]
}
```

---

## Notification

### POST /notification/get

Auth required. No request body.

Response:
```json
{
  "confirmation": "successful",
  "notifications": [
    {
      "notification_id": "string",
      "article_id": "string",
      "article_title": "string",
      "tags": ["string"],
      "created_at": "string"
    }
  ]
}
```

Notifications are sorted newest first. Expired notifications are removed on fetch. Expiry is controlled by `NOTIFICATION_TTL_DAYS` env var (default 30 days).

---

## User

### POST /user/get_all

Auth required. Admin only. No request body.

Response:
```json
{
  "confirmation": "successful",
  "users": [
    {
      "user_id": "string",
      "username": "string",
      "email": "string",
      "fullname": "string",
      "role": "string",
      "report_count": 0,
      "created_at": "string"
    }
  ]
}
```

---

### POST /user/get_details

Auth required.

Request:
```json
{ "user_email": "string or omit" }
```

Regular users can only retrieve their own profile. Omit `user_email` or leave it null to get the requesting user's own profile. Admins can query any user by email.

Response:
```json
{
  "confirmation": "successful",
  "user": {
    "user_id": "string",
    "username": "string",
    "email": "string",
    "fullname": "string",
    "role": "string",
    "created_at": "string",
    "updated_at": "string",
    "reports": []
  }
}
```

`reports` field is only present when the requester is admin.

---

### POST /user/make_admin

Auth required. Admin only.

Request:
```json
{ "user_id": "string" }
```

Response:
```json
{ "confirmation": "successful: role updated to admin" }
```

Possible confirmation values: `successful: role updated to admin`, `already admin`, `user not found`.

---

### POST /user/delete

Auth required. Admin only.

Request:
```json
{ "user_id": "string" }
```

Rules:
- Cannot delete an admin account

Response:
```json
{ "confirmation": "successful: user deleted" }
```

Possible confirmation values: `successful: user deleted`, `user not found`, `cannot delete admin`.

---

## Monitor Harga

### POST /monitor/search

Auth required. Rate limited: 20 requests/minute per IP.

Searches Tokopedia for a product and returns top listings with price and rating. Uses Tokopedia internal GraphQL API — no browser required.

Request:
```json
{
  "product_name": "string",
  "limit": 10
}
```

Rules:
- product_name: 1–200 chars
- limit: integer 1–50, default 10

Response:
```json
{
  "results": [
    {
      "product": "string",
      "store": "string or null",
      "price": 17999000,
      "rating": 5.0
    }
  ],
  "errors": ["string"],
  "total": 10
}
```

- `price` is IDR integer (e.g. `17999000` = Rp17.999.000)
- `rating` is float 0.0–5.0, or null if no reviews
- `errors` lists any per-item parse failures — empty array means all items parsed cleanly
- `total` is count of successfully parsed results

Possible HTTP errors: `401` token missing/invalid, `429` rate limit exceeded, `502` Tokopedia unreachable.

---

### GET /monitor/health

No auth required.

Response:
```json
{ "status": "ok" }
```

---

## General Error Responses

Any protected endpoint returns HTTP 401 when the token is missing or invalid. The backend does not return 401 in the response body — it returns it as the HTTP status code directly.

When a route encounters an unexpected failure it returns:
```json
{ "confirmation": "backend error" }
```

---

## Warnings

All IDs (`article_id`, `comment_id`, `rating_id`, `user_id`) are MongoDB ObjectId strings (24-character hex). Sending a malformed ID returns `backend error`.

Images are stored as binary in the database and returned as base64 strings. The frontend must encode images to base64 before sending and decode base64 back to display. Only PNG and JPEG are accepted.

Article tags are always stored as a list of strings, even if there is only one tag. Never send `article_tags` as a plain string.

The subscription limit per user is 20 tags. Attempting to subscribe beyond this returns `limit reached`.

Notifications are pull-based. The frontend must call `/notification/get` to check for new notifications. There is no push or webhook.

Comment and rating responses return the full article view. The frontend can use this to refresh the article page in a single request instead of calling `/article/view` again.

Regular users cannot access `/article/edit/get`, `/article/edit/update`, `/article/add`, `/article/delete`, `/article/verification`, `/user/get_all`, `/user/make_admin`, or `/user/delete`. These return `{ "confirmation": "not admin" }` for non-admin tokens.

A regular user querying `/user/get_details` with another user's email returns `{ "confirmation": "backend error" }`, not a 403.

The `make_admin` action is irreversible through the API. There is no endpoint to demote an admin back to user.
