# My Family Tree API
Это приложение работает на основе базы данных сервиса webtrees, надо передать подключение к БД и тогда можно будет редактировать данные в обоих приложениях.



## Prepare
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
select uuid_generate_v4()
```
## Generate Secret Key
Для генерации секретного слова в JWT лучше использовать вот эту команду:
```bash
openssl rand -hex 333
```

## Сущности:
- 0: `Root`: Может создавать/удалять `Admin`
- 1: `Admin`: Имеет доступ ко всем параметрам и настройкам
- 2: `account`: Это пользователь у которого есть доступ к приложению (есть логин и пароль). Он может быть связан с `person`
- 3: `person`: Это член какой-то семьи

## Роли:
- `family_member`: Прямой участник какой-то семьи (один шаг к связанной персоне, родитель/ребенок/партнер)
- `close_relative`: Связь между персонами через члена семьи (2-3 шага к связанной персоне).
- `distant_relative`: Связь между персонами через близкого или дальнего родственника (от 3х шагов к связанной персоне)
- `ancestor`: Связь с `person` по родительской линии
- `descendant`: Связь с `person` по линии потомков

## Права доступа:
- `read`: `account`, `person`
- `write`: `person`
- `confirm`: Подтвердить/Отклонить/Изменить правки от другого `person`

Каждый `person` несет ответственность за свой участок дерева. Это определяет роль, которую назначает `Admin`

## Подтвердить/Отклонить/Изменить правки
Любой `person` может внести изменения в любом `person` но подтвердить/отменить/изменить правки может члени семьи или близкий родственник у которого есть `account`. 

### Поиск `account` среди `person`:
- `family_member` -> `close_relative` -> `Admin`
  > Поиск `account` среди `family_member` если не нашел, `close_relative`, если нет `Admin`

## TODO:
Вкорячить новый pydantic и научиться с ним работать. Переделать все схемы на нвый лад. Раскурить новую документацию.
