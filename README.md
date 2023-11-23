# Deliveri_API
## Запуск:
# 1) собрать контейнер
Проверьте файлы .env и .env-non-dev и поменяйте переменные окружения под себя.  
docker-compose up;  
Сервис будет доступен по адресу:  
http://localhost:8001/docs

# 2) создать базу данных для тестов
docker exec -i postgres psql -h localhost -p 5432 -U postgres -d Delivery -c "CREATE DATABASE Delivery_test;"  

# 3) запустить тесты
docker exec -i delivery pytest tests -s  
