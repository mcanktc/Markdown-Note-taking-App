# Markdown Note-Taking API

This is a Django REST Framework-based API that allows users to create, edit, delete, and render Markdown notes. It also provides grammar checking functionality using LanguageTool.

## Features

- Register and login (Django default auth)
- Create notes using plain text or `.md` files
- Auto-convert plain text to `.md` files
- Grammar check on demand
- Render Markdown as HTML in browser

---

> LanguageTool requires Java installed.

---

## API Endpoints

> All endpoints require authentication. Use token or session login.

### Notes

| Method | Endpoint                | Description                               |
| ------ | ----------------------- | ----------------------------------------- |
| GET    | `/notes/`               | List all notes of the authenticated user  |
| POST   | `/notes/`               | Create a new note                         |
| GET    | `/notes/<pk>/`          | Retrieve a single note with grammar check |
| PUT    | `/notes/<pk>/`          | Update a note                             |
| DELETE | `/notes/<pk>/`          | Delete a note                             |
| GET    | `/notes/<pk>/rendered/` | Render Markdown as HTML                   |

---

## Sample Note POST JSON

```json
{
  "title": "Example Note",
  "text": "He go to school every day.",
  "take_type": "T"
}
```

---

## Grammar Checking

* Automatically triggered on:

  * `GET /notes/<pk>/`
  * `PUT /notes/<pk>/`

Returns grammar issues using LanguageTool.

---

## Markdown Rendering

* `GET /notes/<pk>/rendered/`
* Renders Markdown file as HTML using `markdown2`
* Returns a raw HTML page for the browser

---

## File Upload Location

* Markdown files saved under:

  ```
  media/notes/user_<user_id>/note_<note_id>.md
  ```

---