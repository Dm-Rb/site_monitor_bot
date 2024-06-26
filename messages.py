from config import read_ini_file


config = read_ini_file()

messages = {
    'start_message':
        f'Этот бот будет уведомлять вас о проблемах в работе сервера <a href="{config["url"]}"><b><u>{config["display_name"]}</u></b></a>',
    'auth_message':
        'Отправте боту <u>проверочный код авторизации</u> для продолжения',
    'auth_message_exist':
        'Ваш аккаунт уже верифицирован в боте. Для удаления своих данных либо переключения статуса уведомлений используйте команды в меню.',
    'auth_success_message':
        f'Вы верифицированы. Уведомления об неполадках <u>{config["display_name"]}</u> включены',
    'auth_fall_message':
        'Указаный вами код авторизации не верен. Повторите попытку',
    'del_yourself_message_true':
        'Все ваши данные были удалены, бот больше не будет отправлять вам уведомления',
    'del_yourself_message_false':
        'Бот не имеет данных о вас и не отправляет вам уведомлений',
    'check_remzona_not_exist':
        'Пройдите авторизацию (/start)',
    'notifications_on':
        'Уведомления об неполадках веб-сервера remzona.by отключены. Включить уведомления?',
    'notifications_off':
        'Уведомления об неполадках веб-сервера remzona.by включены. Отключить уведомления?'
}








