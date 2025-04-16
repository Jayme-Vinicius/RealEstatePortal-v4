#user.py
from abc import ABC, abstractmethod
class User(ABC):
    def __init__(self, user_id, name, email, password):
        self._id = user_id
        self._name = name
        self._email = email
        self._password = password

    # Getters e setters
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("O nome não pode ser vazio.")
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not value:
            raise ValueError("O email não pode ser vazio.")
        self._email = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if not value:
            raise ValueError("A senha não pode ser vazia.")
        self._password = value

    @abstractmethod
    def get_role(self):
        pass

    def __str__(self):
        return f"Usuário: {self._name} ({self._email})"

#agent.py
class Agent(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password)
        self._properties = []

    def add_property(self, property):
        self._properties.append(property)

    def list_properties(self):
        return self._properties

    def get_role(self):
        return "Agente"

#client.py
class Client(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password)
        self._scheduled_visits = []

    def schedule_visit(self, visit):
        self._scheduled_visits.append(visit)

    def list_scheduled_visits(self):
        return self._scheduled_visits

    def get_role(self):
        return "Cliente"

#inquiry.py
class Inquiry:
    def __init__(self, id, client, property, message):
        self._id = id
        self._client = client
        self._property = property
        self._message = message
        self._status = "Pendente"

    def update_status(self, status):
        self._status = status

    def __str__(self):
        return f"Consulta #{self._id} - {self._property.title} | Status: {self._status}"

class InquiryController:
    def __init__(self):
        self._inquiries = []

    def add_inquiry(self, client, property, message):
        new_inquiry = Inquiry(len(self._inquiries) + 1, client, property, message)
        self._inquiries.append(new_inquiry)
        return new_inquiry

    def list_inquiries(self):
        return [inquiry for inquiry in self._inquiries]

# market_analysis.py
class MarketAnalysis:
    def __init__(self, property_controller):
        self.property_controller = property_controller  
        self._data = []  

    def add_data(self, data_point):
        self._data.append(data_point)

    def get_average_price(self):
        if not self._data:
            return 0
        return sum(self._data) / len(self._data)

    def analyze_prices_by_location(self, location):
        # Pesquisa propriedades por localização
        properties_in_location = [prop for prop in self.property_controller._properties if prop.location == location]

        if not properties_in_location:
            return None  

        # Cálculo de preços médios, mínimos e máximos
        total_price = sum(prop.price for prop in properties_in_location)
        average_price = total_price / len(properties_in_location)
        min_price = min(properties_in_location, key=lambda x: x.price).price
        max_price = max(properties_in_location, key=lambda x: x.price).price

        return {
            "average_price": average_price,
            "min_price": min_price,
            "max_price": max_price,
            "num_properties": len(properties_in_location)
        }

    def count_properties_by_status(self, location, property_type=None):
        # Conta o número de propriedades disponíveis em um local, podendo filtrar por tipo (venda ou aluguel)
        properties_in_location = [prop for prop in self.property_controller._properties if prop.location == location]

        if property_type:
            properties_in_location = [prop for prop in properties_in_location if prop.property_type == property_type]

        available_properties = [prop for prop in properties_in_location if prop.available]
        return len(available_properties)

    def market_analysis(self, location):
        # Obtém a análise de preços e o número de propriedades disponíveis para venda e aluguel
        price_analysis = self.analyze_prices_by_location(location)
        num_available_sale = self.count_properties_by_status(location, "sale")
        num_available_rent = self.count_properties_by_status(location, "rent")

        if price_analysis:
            print(f"\n===== Análise de Mercado para {location} =====")
            print(f"Preço Médio: R${price_analysis['average_price']:.2f}")
            print(f"Preço Mínimo: R${price_analysis['min_price']:.2f}")
            print(f"Preço Máximo: R${price_analysis['max_price']:.2f}")
            print(f"Número de Propriedades: {price_analysis['num_properties']}")
        else:
            print(f"\nNão há propriedades na localização '{location}'.")

        print(f"\nImóveis Disponíveis para Venda: {num_available_sale}")
        print(f"Imóveis Disponíveis para Aluguel: {num_available_rent}")

    def __str__(self):
        return f"Análise de Mercado: Preço Médio = R${self.get_average_price():.2f}"

#mortgage.py
class Mortgage:
    def __init__(self, loan_amount, annual_rate, years):
        # Validação básica das entradas
        if loan_amount <= 0:
            raise ValueError("O valor do empréstimo deve ser positivo.")
        if annual_rate < 0:
            raise ValueError("A taxa anual não pode ser negativa.")
        if years <= 0:
            raise ValueError("O prazo deve ser positivo.")

        # Atribui os valores diretamente
        self.loan_amount = loan_amount
        self.annual_rate = annual_rate
        self.years = years

        # Calcula os valores iniciais
        self.months = years * 12
        self.monthly_payment = self._calculate_monthly_payment()
        self.total_payment = self._calculate_total_payment()

    def _calculate_monthly_payment(self):
        rate = self.annual_rate / 100 / 12
        if rate == 0:
            return self.loan_amount / self.months
        return (self.loan_amount * rate) / (1 - (1 + rate) ** -self.months)

    def _calculate_total_payment(self):
        return self.monthly_payment * self.months

    def __str__(self):
        return (
            f"Parcela mensal: R${self.monthly_payment:.2f}\n"
            f"Total a ser pago: R${self.total_payment:.2f}"
        )

#property.py
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="myGeocoder")

# PropertyFactory.py
class PropertyCreator(ABC): #Interface abstrata para criadores de propriedades
    @abstractmethod
    def create_property(self, property_id, title, description, price, location, transaction_type, agent, virtual_tour_url=None): #Método abstrato para criar uma propriedade
        pass

class HouseCreator(PropertyCreator): #Cria propriedades do tipo Casa
    def create_property(self, property_id, title, description, price, location, transaction_type, agent, virtual_tour_url=None):
        return Property(
            id = property_id,
            title = title,
            description = description,
            price = price,
            location = location,
            property_category = "Casa",
            transaction_type = transaction_type,
            agent = agent,
            virtual_tour_url = virtual_tour_url
        )

class ApartmentCreator(PropertyCreator): #Cria propriedades do tipo Apartamento
    def create_property(self, property_id, title, description, price, location, transaction_type, agent, virtual_tour_url=None):
        return Property(
            id = property_id,
            title = title,
            description = description,
            price=price,
            location = location,
            property_category = "Apartamento",
            transaction_type = transaction_type,
            agent = agent,
            virtual_tour_url = virtual_tour_url
        )

class LandCreator(PropertyCreator): #Cria propriedades do tipo Terreno
    def create_property(self, property_id, title, description, price, location, transaction_type, agent, virtual_tour_url=None):
        return Property(
            id = property_id,
            title = title,
            description = description,
            price = price,
            location = location,
            property_category = "Terreno",
            transaction_type = transaction_type,
            agent = agent,
            virtual_tour_url = virtual_tour_url
        )

class PropertyFactory:
    "Fábrica que seleciona e utiliza o criador apropriado"
    
    @staticmethod
    def get_property_creator(property_type):
        "Retorna o criador adequado para o tipo de propriedade"
        creators = {
            "Casa": HouseCreator(),
            "Apartamento": ApartmentCreator(),
            "Terreno": LandCreator()
        }
        
        if property_type not in creators:
            raise ValueError(f"Tipo de propriedade inválido: {property_type}")
        
        return creators[property_type]
    
    @staticmethod
    def create_property(property_type, property_id, title, description, price, location, transaction_type, agent, virtual_tour_url=None):
        "Método de fábrica para criar uma propriedade do tipo especificado"
        creator = PropertyFactory.get_property_creator(property_type)
        return creator.create_property(property_id, title, description, price, location, transaction_type, agent, virtual_tour_url)

class Property:
    def __init__(self, id, title, description, price, location, property_category, transaction_type, agent, virtual_tour_url=None):
        self._id = id
        self.title = title
        self.description = description
        self.price = price
        self.location = location
        self.property_category = property_category
        self.transaction_type = transaction_type
        self._agent = agent
        self._available = True
        self.virtual_tour_url = virtual_tour_url

    # Validações e getters/setters
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value:
            raise ValueError("Título não pode ser vazio.")
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not value:
            raise ValueError("Descrição não pode ser vazia.")
        self._description = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Preço não pode ser negativo.")
        self._price = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        if not value:
            raise ValueError("Localização não pode ser vazia.")
        self._location = value

    @property
    def property_category(self):
        return self._property_category

    @property_category.setter
    def property_category(self, value):
        valid_categories = {"Casa", "Apartamento", "Terreno"}
        if value not in valid_categories:
            raise ValueError(f"Categoria inválida. Use: {valid_categories}")
        self._property_category = value

    @property
    def transaction_type(self):
        return self._transaction_type

    @transaction_type.setter
    def transaction_type(self, value):
        valid_transactions = {"Venda", "Aluguel"}
        if value not in valid_transactions:
            raise ValueError(f"Transação inválida. Use: {valid_transactions}")
        self._transaction_type = value

    # Ajuste para acessar o ID
    @property
    def id(self):
        return self._id

    @property
    def agent(self):
        return self._agent

    @agent.setter
    def agent(self, value):
        if not value:
            raise ValueError("Agente não pode ser vazio.")
        self._agent = value

    @property
    def available(self):
        return self._available

    @available.setter
    def available(self, value):
        if not isinstance(value, bool):
            raise ValueError("Disponibilidade deve ser um valor booleano.")
        self._available = value

    @property
    def virtual_tour_url(self):
        return self._virtual_tour_url

    @virtual_tour_url.setter
    def virtual_tour_url(self, value):
        self._virtual_tour_url = value

    def remove_virtual_tour(self):
        self.virtual_tour_url = None

    def update_details(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

    def switch_status(self):
        self._available = not self._available

    def get_coordinates(self):
        location = geolocator.geocode(self.location)
        if location:
            return location.latitude, location.longitude
        return None, None

    def get_google_maps_link(self):
        latitude, longitude = self.get_coordinates()
        if latitude and longitude:
            return f"https://www.google.com/maps?q={latitude},{longitude}"
        return "Localização não encontrada"

    def __str__(self):
        return (
            f"ID: {self._id}\n"
            f"Propriedade: {self._title}\n"
            f"Descrição: {self._description}\n"
            f"Preço: R${self._price}\n"
            f"Localização: {self._location}\n"
            f"Categoria: {self._property_category}\n"
            f"Transação: {'Venda' if self._transaction_type == 'Venda' else 'Aluguel'}\n"
            f"Disponível: {'Sim' if self._available else 'Não'}\n"
            f"Tour Virtual: {self.virtual_tour_url if self.virtual_tour_url else 'Nenhum'}\n"
        )

#review.py
from datetime import datetime
class Review:
    def __init__(self, property_id, user, rating, comment):
        self._property_id = property_id
        self._user = user
        self._rating = rating
        self._comment = comment
        self._date = datetime.now()

    # Getter para property_id
    @property
    def property_id(self):
        return self._property_id

    # Getters e setters para rating
    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not (1 <= value <= 5):
            raise ValueError("A avaliação deve estar entre 1 e 5.")
        self._rating = value

    # Getters e setters para comment
    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        if not value:
            raise ValueError("O comentário não pode ser vazio.")
        self._comment = value

    # Getter para a data formatada
    @property
    def date(self):
        return self._date.strftime("%Y-%m-%d %H:%M")

    # Método para atualizar a avaliação
    def update_review(self, rating=None, comment=None):
        if rating:
            self.rating = rating  # Usa o setter
        if comment:
            self.comment = comment  # Usa o setter

#Visit.py
class Visit:
    def __init__(self, id, client, agent, property, date_time):
        if not all([client, agent, property, date_time]):
            raise ValueError("Todos os campos (cliente, agente, propriedade, data/hora) são obrigatórios.")
        self._id = id
        self._client = client
        self._agent = agent
        self._property = property
        self._date_time = date_time
        self._status = "Agendado!"

    def __str__(self):
        return f"Visita #{self._id} - {self._property.title} | Data: {self._date_time} | Status: {self._status}"

    # Getters e setters para date_time
    @property
    def date_time(self):
        return self._date_time

    @date_time.setter
    def date_time(self, value):
        if not value:
            raise ValueError("A data e hora não podem ser vazias.")
        self._date_time = value

    # Getter para status (somente leitura)
    @property
    def status(self):
        return self._status

    # Método para reagendar a visita
    def reschedule(self, new_date_time):
        self.date_time = new_date_time  # Usa o setter
        self._status = "Reagendado!"

    # Método para cancelar a visita
    def cancel(self):
        self._status = "Cancelado!"

#database.py
# Simulação de Banco de Dados em Memória
class Database:
    def __init__(self):
        self.users = []         # Lista de usuários (Clientes e Agentes)
        self.properties = []    # Lista de propriedades
        self.visits = []        # Lista de visitas agendadas
        self.reviews = []       # Lista de avaliações
        self._next_property_id = 1

        # Inicializa os dados do banco de dados
        self.initialize_data()

    # Adiciona um novo usuário à lista
    def add_user(self, user: User):
        self.users.append(user)

    # Retorna todos os usuários na lista
    def get_users(self):
        return self.users

    # Retorna apenas os clientes
    def get_clients(self):
        return [user for user in self.users if user.user_type == "Cliente"]

    # Retorna apenas os agentes
    def get_agents(self):
        return [user for user in self.users if user.user_type == "Agente"]

    # Adiciona uma propriedade
    def add_property(self, property: Property):
        # Verifica se já existe uma propriedade com o mesmo título e localização
        if any(prop.title == property.title and prop.location == property.location for prop in self.properties):
            raise ValueError("Propriedade já cadastrada.")

        property._id = self._next_property_id
        self.properties.append(property)
        self._next_property_id += 1

    # Retorna todas as propriedades
    def get_properties(self):
        return self.properties

    # Adiciona uma visita
    def add_visit(self, visit: Visit):
        self.visits.append(visit)

    # Retorna todas as visitas
    def get_visits(self):
        return self.visits

    # Adiciona uma avaliação
    def add_review(self, review: Review):
        self.reviews.append(review)

    # Retorna todas as avaliações
    def get_reviews(self):
        return self.reviews

    # Database inicial de propriedades
    def initialize_data(self):
        # Propriedades predefinidas
        properties = [
            Property(
                id=1,
                title="Casa na Praia",
                description="Linda casa com vista para o mar",
                price=1000000,
                location="Rio de Janeiro",
                property_category="Casa",
                transaction_type="Venda",
                agent="João Silva"
            ),
            Property(
                id=2,
                title="Apartamento no Centro",
                description="Apartamento moderno",
                price=500000,
                location="São Paulo",
                property_category="Apartamento",
                transaction_type="Aluguel",
                agent="Maria Souza"
            ),
            Property(
                id=3,
                title="Terreno Residencial",
                description="Terreno plano e amplo",
                price=300000,
                location="Belo Horizonte",
                property_category="Terreno",
                transaction_type="Venda",
                agent="Carlos Oliveira"
            )
        ]

        # Adiciona as propriedades ao banco de dados
        for prop in properties:
            self.add_property(prop)

# Instância global do banco de dados para ser usada em todo o sistema
db = Database()

#market_analysis_controller.py
class MarketAnalysisController:
    def __init__(self, property_controller):
        self.property_controller = property_controller

    def get_market_analysis(self, location):
        # Obtém todas as propriedades na localização selecionada
        properties = self.property_controller.search_property_by_location(location)

        if not properties:
            return None

        # Filtra propriedades à venda e para aluguel
        properties_for_sale = [p for p in properties if p.transaction_type == "Venda"]
        properties_for_rent = [p for p in properties if p.transaction_type == "Aluguel"]

        # Calcula o preço médio
        total_price = sum(p.price for p in properties)
        avg_price = total_price / len(properties)

        # Conta o número de propriedades à venda e para aluguel
        num_sale = len(properties_for_sale)
        num_rent = len(properties_for_rent)

        return {
            "avg_price": avg_price,
            "num_sale": num_sale,
            "num_rent": num_rent     
        }

#mortgage_controller.py
class MortgageController:
    def calculate_mortgage(self, loan_amount, annual_rate, years):
        calculator = Mortgage(loan_amount, annual_rate, years)
        return calculator

#property_controller.py
class PropertyController:
    def __init__(self):
        self._properties = db.get_properties()

    def add_property(self, property):
        # Verifica se já existe uma propriedade com o mesmo título e localização
        if any(prop.title == property.title and prop.location == property.location for prop in self._properties):
            raise ValueError("Propriedade já cadastrada.")
        db.add_property(property)               # Adiciona a propriedade ao banco de dados
        self._properties = db.get_properties()  # Adiciona a propriedade à lista local
        return property
    
    def create_property(self, property_type, title, description, price, location, transaction_type, agent, virtual_tour_url=None): #Cria uma nova propriedade usando o Factory Pattern
        # Usa o PropertyFactory para criar a propriedade do tipo adequado
        property = PropertyFactory.create_property(
            property_type = property_type,
            property_id = None,  # O ID será atribuído pelo banco de dados
            title = title,
            description = description,
            price = price,
            location = location,
            transaction_type = transaction_type,
            agent = agent,
            virtual_tour_url = virtual_tour_url
        )
        
        # Adiciona a propriedade criada ao banco de dados
        return self.add_property(property)

    def list_properties(self):
        return [vars(prop) for prop in self._properties]

    def find_property_by_id(self, property_id):
        for prop in self._properties:
            if prop.id == property_id:
                return prop
        return None

    def update_property(self, property_id, title=None, description=None, price=None, location=None):
        property_to_update = self.find_property_by_id(property_id)
        if property_to_update:
            property_to_update.update_details(title, description, price, location)
            return property_to_update
        return None

    def delete_property(self, property_id):
        property_to_delete = self.find_property_by_id(property_id)
        if property_to_delete:
            db.properties.remove(property_to_delete)     # Remove do banco de dados
            self._properties.remove(property_to_delete)  # Remove da lista local
            return True
        return False

    def search_all_properties(self):
        return [prop for prop in self._properties]

    def search_property_by_type(self, property_category ):
        return [prop for prop in self._properties if prop.property_category.lower() == property_category.lower()]

    def search_property_by_location(self, location):
        return [prop for prop in self._properties if location.lower() in prop.location.lower()]

    def search_property_by_price_range(self, price_min, price_max):
        return [prop for prop in self._properties if price_min <= prop.price <= price_max]

#review_controller.py
class ReviewController:
    def __init__(self):
        self.reviews = db.get_reviews() # Carrega as avaliações do banco de dados

    def add_review(self, reviewer_id, property_id, rating, comment):
        # Validação da nota
        if rating < 1 or rating > 5:
            raise ValueError("A nota deve estar entre 1 e 5.")

        # Verifica se a propriedade existe (usando PropertyController)
        property_controller = PropertyController()
        if not property_controller.find_property_by_id(property_id):
            raise ValueError("Propriedade não encontrada.")

        # Cria e adiciona a avaliação
        new_review = Review(property_id, reviewer_id, rating, comment)
        db.add_review(new_review)
        return new_review

    def list_reviews(self):
        return [vars(review) for review in db.reviews]

    def find_review_by_id(self, review_id):
        for review in db.reviews:
            if review.id == review_id:
                return review
        return None

    def delete_review(self, review_id):
        review_to_delete = self.find_review_by_id(review_id)
        if review_to_delete:
            db.reviews.remove(review_to_delete)
            return True
        return False

    def list_all_reviews(self):
        return db.get_reviews()

    def get_reviews_by_property(self, property_id):
        return [review for review in db.reviews if review.property_id == property_id]

    def get_average_rating(self, property_id):
        reviews = self.get_reviews_by_property(property_id)
        if not reviews:
            return 0
        total = sum(review.rating for review in reviews)
        return total / len(reviews)

#user_controller.py
class UserController:
    def login(self):
        email = input("Digite seu email: ")
        password = input("Digite sua senha: ")

        # Procura o usuário com o email e senha correspondentes
        user = next((user for user in db.get_users() if user.email == email and user.password == password), None)

        if user:
            print(f"Login realizado com sucesso! Bem-vindo, {user.name}.")
            return user  # Retorna o usuário logado
        else:
            print("Erro: Email ou senha incorretos.")
            return None

    # Cadastra um novo usuário
    def register_user(self, name, email, password, user_type):
        # Valida o tipo de usuário
        valid_types = ["Cliente", "Agente"]
        if user_type.capitalize() not in valid_types:
            print(f"Erro: Tipo de usuário inválido. Escolha entre {valid_types}.")
            return None

        # Verifica se o email já foi cadastrado
        if any(user.email == email for user in db.get_users()):
            print(f"Erro: O email {email} já está em uso.")
            return None

        # Cria um novo usuário (instanciando Client ou Agent)
        if user_type.capitalize() == "Cliente":
            new_user = Client(len(db.get_users()) + 1, name, email, password)
        elif user_type.capitalize() == "Agente":
            new_user = Agent(len(db.get_users()) + 1, name, email, password)

        # Adiciona o novo usuário ao banco de dados
        db.add_user(new_user)
        print(f"Usuário {name} registrado com sucesso como {user_type.capitalize()}!")
        return new_user

    # Lista todos os usuários
    def list_users(self):
        users = db.get_users()
        if not users:
            print("Nenhum usuário cadastrado.")
        for user in users:
            print(user)

    # Deleta um usuário pelo ID
    def delete_user(self, user_id):
        users = db.get_users()
        user_to_delete = next((user for user in users if user.id == user_id), None)
        if user_to_delete:
            db.users.remove(user_to_delete)
            print(f"Usuário {user_to_delete.name} excluído com sucesso.")
            return True
        print(f"Erro: Usuário com ID {user_id} não encontrado.")
        return False

    # Lista apenas os clientes
    def list_clients(self):
        clients = db.get_clients()
        if not clients:
            print("Nenhum cliente cadastrado.")
        for client in clients:
            print(client)

    # Lista apenas os agentes
    def list_agents(self):
        agents = db.get_agents()
        if not agents:
            print("Nenhum agente cadastrado.")
        for agent in agents:
            print(agent)

    def find_user_by_id(self, user_id):
        for user in db.get_users():
            if user.id == user_id:
                return user
        return None

#visit controller
class VisitController:
    def __init__(self, property_controller, user_controller):
        self.property_controller = property_controller  # Instância de PropertyController
        self.user_controller = user_controller  # Instância de UserController

    def schedule_visit(self, id, client_id, property_id, date_time):
        # Busca a propriedade usando o PropertyController
        property_obj = self.property_controller.find_property_by_id(property_id)
        if not property_obj:
            raise ValueError("Propriedade não encontrada.")

        # Obtém o agente associado à propriedade
        agent = property_obj.agent  # Supondo que a propriedade tenha um atributo 'agent'

        # Busca o cliente usando o UserController
        client = self.user_controller.find_user_by_id(client_id)
        if not client:
            raise ValueError("Cliente não encontrado.")

        # Cria a visita
        new_visit = Visit(id, client, agent, property_obj, date_time)
        db.add_visit(new_visit)
        return new_visit

    def list_visits(self):
        return db.get_visits()  # Retorna todas as visitas do banco de dados

    def find_visit_by_id(self, visit_id):
        for visit in db.get_visits():
            if visit._id == visit_id:
                return visit
        return None

    def cancel_visit(self, visit_id):
        visit_to_cancel = self.find_visit_by_id(visit_id)
        if visit_to_cancel:
            visit_to_cancel.cancel()  # Altera o status para "Cancelado!"
            return True
        return False

    def reschedule_visit(self, visit_id, new_date_time):
        visit_to_reschedule = self.find_visit_by_id(visit_id)
        if visit_to_reschedule:
            visit_to_reschedule.reschedule(new_date_time)  # Reagenda a visita
            return True
        return False

#main.py
def agendamento_menu(logged_user, visit_controller):
    while True:
        print("\n===== Agendamento de Compromissos =====")
        print("1. Agendar visita")
        print("2. Listar visitas marcadas")
        print("3. Cancelar visita")
        print("4. Reagendar visita")
        print("5. Voltar ao menu principal")
        option = input("Escolha uma opção: ")

        if option == "1":
            print("\n===== Agendar Visita =====")
            if logged_user is None:
                print("Erro: Nenhum usuário logado.")
            else:
                property_id = int(input("Digite o ID da propriedade para agendar visita: "))
                date_time = input("Digite a data e hora para a visita (ex: 2025-03-14 10:00): ")

                # Agendar visita
                try:
                    new_visit = visit_controller.schedule_visit(
                        id=len(db.get_visits()) + 1,
                        client_id=logged_user.id,
                        property_id=property_id,
                        date_time=date_time
                    )
                    print(f"Visita agendada com sucesso!\n{new_visit}")
                except ValueError as e:
                    print(f"Erro ao agendar a visita: {e}")

        elif option == "2":
            print("\n===== Visitas Marcadas =====")
            visits = visit_controller.list_visits()
            if visits:
                for visit in visits:
                    print(visit)
            else:
                print("Nenhuma visita marcada.")

        elif option == "3":
            visit_id = int(input("Digite o ID da visita que deseja cancelar: "))
            if visit_controller.cancel_visit(visit_id):
                print("Visita cancelada com sucesso.")
            else:
                print("Visita não encontrada.")

        elif option == "4":
            visit_id = int(input("Digite o ID da visita que deseja reagendar: "))
            new_date_time = input("Digite a nova data e hora (ex: 2025-03-15 14:00): ")
            if visit_controller.reschedule_visit(visit_id, new_date_time):
                print("Visita reagendada com sucesso.")
            else:
                print("Visita não encontrada.")

        elif option == "5":
            break  # Volta ao menu principal

        else:
            print("Opção inválida. Tente novamente.")

def menu():
    user_controller = UserController()
    property_controller = PropertyController()
    mortgage_controller = MortgageController()
    visit_controller = VisitController(property_controller, user_controller)
    market_analysis_controller = MarketAnalysisController(property_controller)
    review_controller = ReviewController()
    logged_user = None

    while True:
        try:
            print("\n===== Portal de Imóveis =====")
            print("1 - Cadastrar Usuário")
            print("2 - Login")
            print("3 - Cadastrar Propriedade")
            print("4 - Buscar Propriedades")
            print("5 - Calcular Financiamento")
            print("6 - Agendar visita")
            print("7 - Avaliar Propriedade")
            print("8 - Exibir Avaliações")
            print("9 - Análise de Mercado")
            print("10 - Logout")
            print("0 - Sair")

            option = input("Escolha uma opção: ")

            if option == "1":
                name = input("Digite o nome do usuário: ")
                email = input("Digite o email do usuário: ")
                password = input("Digite a senha: ")
                user_type = input("Digite o tipo de usuário (Cliente ou Agente): ")
                user_controller.register_user(name, email, password, user_type)

            elif option == "2":
                logged_user = user_controller.login()

            elif option == "3":
                if logged_user is None:
                    print("Erro: Nenhum usuário logado.")
                elif logged_user.get_role() != "Agente":
                    print("Erro: Apenas agentes podem cadastrar uma propriedade.")
                else:
                    title = input("Digite o título da propriedade: ")
                    description = input("Digite a descrição da propriedade: ")
                    price = float(input("Digite o preço da propriedade: "))
                    location = input("Digite a localização da propriedade: ")
                    property_category = input("Digite o tipo do imóvel (Casa/Apartamento/Terreno): ").capitalize()
                    while property_category not in {"Casa", "Apartamento", "Terreno"}:
                        print("Erro: Categoria inválida. Use: Casa, Apartamento ou Terreno.")
                        property_category = input("Digite o tipo do imóvel (Casa/Apartamento/Terreno): ")
                    transaction_type = input("Digite o tipo de transação (Venda/Aluguel): ").capitalize()
                    while transaction_type not in {"Venda", "Aluguel"}:
                        print("Erro: Transação inválida. Use: Venda ou Aluguel.")
                        transaction_type = input("Digite o tipo de transação (Venda/Aluguel): ")
                    # Usa o Factory Method para criar a propriedade
                    new_property = property_controller.create_property(
                        property_type = property_category,
                        title = title,
                        description = description,
                        price = price,
                        location = location,
                        transaction_type = transaction_type,
                        agent = logged_user
                    )
                    print(f"Propriedade '{new_property.title}' cadastrada com sucesso!")

            elif option == "4":
                print("\n===== Buscar Propriedades =====")
                search_by = input("Buscar por: 0 - Todas | 1 - Localização | 2 - Tipo | 3 - Faixa de preço: ")
                if search_by == "0":
                    results = property_controller.search_all_properties()
                elif search_by == "1":
                    location = input("Digite a localização: ")
                    results = property_controller.search_property_by_location(location)
                elif search_by == "2":
                    property_category = input("Digite o tipo do imóvel (Casa/Apartamento/Terreno): ")
                    results = property_controller.search_property_by_type(property_category)
                elif search_by == "3":
                    min_price = float(input("Digite o preço mínimo: "))
                    max_price = float(input("Digite o preço máximo: "))
                    results = property_controller.search_property_by_price_range(min_price, max_price)
                else:
                    print("Opção inválida.")
                    return
                if results:
                    print("\nResultados da busca:")
                    for prop in results:
                        print(prop)
                else:
                    print("Nenhuma propriedade encontrada.")

            elif option == "5":
                print("\n===== Calcular Financiamento =====")
                price = float(input("Digite o preço do imóvel: "))
                interest_rate = float(input("Digite a taxa de juros anual (em %): "))
                years = int(input("Digite o período de pagamento (em anos): "))

                mortgage = mortgage_controller.calculate_mortgage(price, interest_rate, years)

                print(f"\nValor da parcela mensal: R$ {mortgage.monthly_payment:.2f}")
                print(f"Valor total do financiamento: R$ {mortgage.total_payment:.2f}")

            elif option == "6":
                agendamento_menu(logged_user, visit_controller)  # Chama o menu de agendamento

            elif option == "7":
                print("\n===== Avaliar Propriedade =====")
                if logged_user is None:
                    print("Erro: Nenhum usuário logado.")
                else:
                    property_id = int(input("Digite o ID da propriedade para avaliar: "))
                    rating = float(input("Digite a nota de avaliação (1-5): "))
                    comment = input("Digite um comentário (opcional): ")
                    # Adicionar avaliação usando o ReviewController
                    new_review = review_controller.add_review(
                        reviewer_id=logged_user.id,
                        property_id=property_id,
                        rating=rating,
                        comment=comment
                    )
                    if new_review:
                        print("Avaliação adicionada com sucesso!")
                    else:
                        print("Erro ao adicionar a avaliação.")

            elif option == "8":
                print("===== Exibir Avaliações =====")
                reviews = review_controller.list_all_reviews()
                if reviews:
                    print("Todas as avaliações cadastradas:")
                    for review in reviews:
                        print(
                            f"\nPropriedade ID: {review.property_id}, "
                            f"\nNota: {review.rating}, "
                            f"\nComentário: {review.comment}, "
                            f"\nData: {review.date}"
                        )
                else:
                    print("Nenhuma avaliação cadastrada.")

            elif option == "9":
                print("\n===== Análise de Mercado =====")
                location = input("Digite a localização para análise de mercado: ")
                analysis = market_analysis_controller.get_market_analysis(location)

                if analysis:
                    print(f"\nPreço Médio: R$ {analysis['avg_price']:.2f}")
                    print(f"Número de Imóveis para Venda: {analysis['num_sale']}")
                    print(f"Número de Imóveis para Aluguel: {analysis['num_rent']}")
                else:
                    print("Nenhuma análise disponível para esta localização.")

            elif option == "10":
                if logged_user:
                    print(f"Logout realizado. Até mais, {logged_user.name}!")
                    logged_user = None
                else:
                    print("Nenhum usuário logado.")

            elif option == "0":
                print("Saindo do sistema...")
                break

            else:
                print("Opção inválida. Tente novamente.")

        except Exception as e:
            print(f"\nErro inesperado: {e}")
            print("Voltando ao menu principal...")

if __name__ == "__main__":
    menu()