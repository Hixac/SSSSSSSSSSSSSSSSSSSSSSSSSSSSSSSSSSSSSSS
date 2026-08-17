import type { Translation } from './en';

const ru: Translation = {
  common: {
    logout: 'Выйти',
  },
  auth: {
    signIn: 'Войти',
    signUp: 'Зарегистрироваться',
    email: 'Почта',
    password: 'Пароль',
    confirmPassword: 'Подтвердите пароль',
    signInSubtitle: 'manyS — планировщик контента ВК',
    signupSubtitle: 'Начните планировать контент для ваших групп ВК',
    fillAllFields: 'Заполните все поля',
    atLeast8: 'Минимум 8 символов',
    passwordMin8: 'Пароль должен содержать минимум 8 символов',
    passwordsMismatch: 'Пароли не совпадают',
    noAccount: 'Нет аккаунта?',
    haveAccount: 'Уже есть аккаунт?',
  },
  board: {
    wallPosts: 'Записи со стены',
    postponed: 'Отложенные',
  },
  group: {
    group: 'Группа',
    domain: 'Домен группы ВК',
    load: 'Загрузить',
  },
  feed: {
    noPosts: 'Записи этой группы не найдены.',
    all: 'Это всё',
    scrollMore: 'Прокрутите вниз, чтобы загрузить ещё',
  },
  post: {
    pinned: 'Закреплено',
    fallback: 'Запись',
  },
  postponed: {
    title: 'Отложенные записи',
    text: 'Текст',
    attachMedia: 'Прикрепить медиа',
    removeFile: 'Убрать файл',
    schedule: 'Запланировать',
    nothingYet: 'Пока ничего не отложено.',
    mediaOnly: '(только медиа)',
    enterTextOrFile: 'Введите текст или прикрепите файл',
    created: 'Отложенная запись создана',
  },
  errors: {
    requestFailed: 'Ошибка запроса ({{status}})',
    unexpected: 'Неожиданная ошибка',
  },
};

export default ru;
