# Chess API

Healthiness probe: `/healtz` \
Readiness probe: `/readyz` \
Publication readiness probe: `/publication/ready` \
Version: `/version` \
Prefix: `/api/v1` \
Authorization: `Bearer {token}` - подставляется `id_token` из Google OAuth2

## Boards

### Schemas

#### BoardRead

```json
{
  "uuid": "some-uuid",
  "owner": "some-uuid",
  "mode": "online",
  "privacy": "private",
  "invited": "some-uuid",
  "created_at": "some-datetime",
  "status": "progress",  // "progress" | "check" | "checkmate" | "stalemate"
  "state": {
    "a1": "queen_owner",
    "e5": "king_invited"
  }
}
```

#### BoardCreate

```json
{
  "owner": "some-uuid",
  "mode": "online",
  "privacy": "private"
}
```

### Endpoints

**POST** `/boards` - создает доску

Request: BoardCreate

Response:

```json
{
  "data": "some-uuid",
  "detail": "Board was added."
}
```

**PUT** `/boards/some-uuid/invited` - добавляет второго игрока к доске

Request:

```json
{
  "invitation": "some-six-digit-code",
  "invited": "some-uuid"
}
```

Response:

```json
{
  "data": "some-uuid",
  "detail": "Board was updated."
}
```

**GET** `/boards` - возвращает доски

Query params:

- `owner` - указать, чтобы получить доски конкретного пользователя
- `invited` - указать, получить доски, где пользователь является вторым игроком

Request: Empty

Response:

```json
{
  "data": [
    BoardRead,
    BoardRead,
    ...
  ],
  "detail": "Boards were selected."
}
```

## Invitations

### Schemas

#### InvitationCreate

```json
{
  "board": "some-uuid"
}
```

### Endpoints

**POST** `/invitations` - создает пригласительный код

Request: InvitationCreate

Response:

```json
{
  "data": "some-six-digit-code",
  "detail": "Invitation was added."
}
```

## Moves

### Schemas

#### MoveRead

```json
{
  "uuid": "some-uuid",
  "board": "some-uuid",
  "actor": "owner",  // "owner" | "invited"
  "created_at": "some-datetime",
  "src": "a1",
  "dst": "a3",
  "figure": "queen"
}
```

#### MoveCreate

```json
{
  "board": "some-uuid",
  "actor": "invited",
  "src": "a1",
  "dst": "a3"
}
```

### Endpoints

**POST** `/moves` - создает ход

Request: MoveCreate

Response:

```json
{
  "data": "some-uuid",
  "detail": "Move was added."
}
```

**GET** `/moves` - возвращает ходы

Query params:

- `board` - указать, чтобы получить ходы на конкретной доске
- `actor` - указать, чтобы получить ходы владельца или приглашенного игрока

Request: Empty

Response:

```json
{
  "data": [
    MoveRead,
    MoveRead,
    ...
  ],
  "detail": "Moves were selected."
}
```

**DELETE** `/moves/last` - отменяет последний ход

Request:

```json
{
  "actor": "owner"  // "owner" | "invited"
}
```

Response:

```json
{
  "data": "some-uuid",
  "detail": "Move was deleted."
}
```
