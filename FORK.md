# Как создать форк на GitHub

Проект: **Soft Braille Keyboard**  
Репозиторий: https://github.com/danieldalton10/Soft-Braille-Keyboard

## Способ 1: через веб-интерфейс GitHub

1. Откройте https://github.com/danieldalton10/Soft-Braille-Keyboard
2. Нажмите кнопку **Fork** в правом верхнем углу
3. Выберите свой аккаунт GitHub — форк будет создан в `https://github.com/YOUR_USERNAME/Soft-Braille-Keyboard`

## Способ 2: через Git в терминале

Если у вас уже есть локальная копия:

```bash
# 1. Перейдите в папку проекта
cd d:\Soft-Braille-Keyboard

# 2. Создайте репозиторий на GitHub (через сайт github.com: New repository)

# 3. Добавьте свой репозиторий как новый remote
git remote add myfork https://github.com/YOUR_USERNAME/Soft-Braille-Keyboard.git

# 4. Запушьте текущую ветку
git push -u myfork master
```

Замените `YOUR_USERNAME` на ваш логин GitHub.

## Способ 3: клонирование и пуш

```bash
# 1. Клонируйте оригинал
git clone https://github.com/danieldalton10/Soft-Braille-Keyboard.git
cd Soft-Braille-Keyboard

# 2. Создайте репозиторий на github.com (пустой, без README)

# 3. Смените remote на свой форк
git remote set-url origin https://github.com/YOUR_USERNAME/Soft-Braille-Keyboard.git

# 4. Отправьте код
git push -u origin master
```
