ci/cd микро-сервисного приложения "app"


Примерный Flow:
1. разработчик выкладывает source приложения ./app в gitlab
2. запускается pipeline, который клонирует ci/cd скрипты отдельного репо
3. собирается docker-контейнер "app" и делается его юнит тест
4. развертывается микро-сервисное окружение вместе с "app"
5. ручное тестирование, затем создается merge-request  
6. commit merge-request 


cписок микро-сервисов:
   api - сервер
   app - клиент
   postgres - для хранения пользовательских операций 
   redis - кэш
   worker - процессинг (вычисляет числа Фибоначчи)
   nginx - роутинг к app/api
 Юнит тест:
   внутренние скрипты в приложении "app": App.test.js
 Интеграционный тест:
   через helm деплоится custom resource: "CI", который в свою очередь вызывает kubernetes operator
   для развертывания микро-сервисного окружения
   Чекинг:
       check-finish.sh - чек-скрипт проверяет, что все микро-сервисы развернулись: exit 0 - success, exit 1 - failed
           $TEST_DURATION_SEC - время, отведенное на проверку 
           $TMP_NAMESPACE - временный namespace для микро-сервисов
 
Директории:
./app - тестируемое приложение
./ci-chart - helm-chart для параметризации CI: custom-resource
./

Микро

WORKFLOW:

Преднастройки
1. настрой Gitlab CI/CD Kubernetes
2. настрой Gitlab Runners: Kubernetes (tag: kuber) + Shell (tag: micro-shell)
3. создай repo
Запуск:
1. comm

cd ./app
docker build -t client -f ../docker/Dockerfile.dev .
docker run client npm run test -- --coverage
echo $?




