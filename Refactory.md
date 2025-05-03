
# Aplicação dos Padrões de Projeto: Factory Method, Facade e Observer

## Introdução

O sistema de gerenciamento imobiliário desenvolvido utiliza três padrões de projeto clássicos — **Factory Method**, **Facade** e **Observer** — para alcançar maior modularidade, extensibilidade e desacoplamento entre os componentes. Este documento explica os motivos por trás da escolha desses padrões, como cada um foi implementado, com exemplos de código, e como contribuem para o funcionamento geral do sistema.

---

## 1. Factory Method

### Objetivo

O padrão **Factory Method** é usado para encapsular a criação de objetos, permitindo que subclasses decidam qual classe instanciar. Ele fornece uma interface para criar objetos em uma superclasse, mas permite que as subclasses modifiquem o tipo de objeto que será criado.

### Por que foi utilizado?

Antes da refatoração, objetos `Property` eram criados diretamente no controlador e na interface gráfica, resultando em:

- **Acoplamento forte** com a classe `Property`.
- **Baixa extensibilidade**, dificultando a adição de novos tipos de propriedades.
- **Código repetitivo** e lógica de criação espalhada.

### Implementação

**Interface base:**

```python
class PropertyCreator(ABC):
    @abstractmethod
    def create_property(self, property_id, title, description, price, location, transaction_type, agent, virtual_tour_url=None):
        pass
```

**Implementações concretas:**

```python
class HouseCreator(PropertyCreator):
    def create_property(...):
        return Property(property_category="Casa", ...)

class ApartmentCreator(PropertyCreator):
    def create_property(...):
        return Property(property_category="Apartamento", ...)
```

**Fábrica central:**

```python
class PropertyFactory:
    @staticmethod
    def get_property_creator(property_type):
        creators = {
            "Casa": HouseCreator(),
            "Apartamento": ApartmentCreator(),
            "Terreno": LandCreator()
        }
        return creators[property_type]

    @staticmethod
    def create_property(...):
        creator = PropertyFactory.get_property_creator(property_type)
        return creator.create_property(...)
```

**Uso no controlador:**

```python
def create_property(self, property_type, ...):
    property = PropertyFactory.create_property(...)
    return self.add_property(property)
```

### Benefícios

- Redução de acoplamento.
- Facilidade de manutenção e testes.
- Extensibilidade com pouco esforço.

---

## 2. Facade

### Objetivo

O padrão **Facade** fornece uma interface unificada para um conjunto de interfaces em um subsistema. Ele define uma interface de alto nível que torna o subsistema mais fácil de usar.

### Por que foi utilizado?

A interface gráfica precisaria interagir com diversos controladores diretamente, o que aumentaria o acoplamento. Com a fachada, centralizamos essa comunicação.

### Implementação

```python
class SystemFacade:
    def __init__(self):
        self.user_controller = UserController(...)
        self.property_controller = PropertyController(...)
        self.transaction_controller = TransactionController(...)

    def register_user(self, ...):
        return self.user_controller.register(...)

    def create_property(self, property_type, ...):
        return self.property_controller.create_property(property_type, ...)
```

### Uso

Na camada de interface, ao invés de chamar diretamente múltiplos controladores:

```python
facade = SystemFacade()
facade.create_property("Casa", ...)
```

### Benefícios

- Interface gráfica desacoplada da lógica de negócio.
- Substituição de múltiplas dependências por uma só.
- Facilidade de manutenção.

---

## 3. Observer

### Objetivo

O padrão **Observer** define uma dependência um-para-muitos entre objetos, de forma que quando um objeto muda de estado, todos os seus dependentes são notificados automaticamente.

### Por que foi utilizado?

O sistema exige reações a eventos como criação de propriedades ou conclusão de transações. Ao invés de acoplamento direto, os observers lidam com essas reações.

### Implementação

**Interface Observer:**

```python
class Observer(ABC):
    @abstractmethod
    def update(self, event_type, data):
        pass
```

**Sujeito observável (por exemplo, PropertyController):**

```python
class PropertyController:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify(self, event_type, data):
        for obs in self.observers:
            obs.update(event_type, data)

    def create_property(self, ...):
        # criação da propriedade
        self.notify("property_created", new_property)
```

**Observer concreto:**

```python
class LoggerObserver(Observer):
    def update(self, event_type, data):
        if event_type == "property_created":
            print(f"Log: Nova propriedade criada: {data.title}")
```

### Benefícios

- Baixo acoplamento entre emissores e ouvintes.
- Extensibilidade sem alterar o código base.
- Clareza na separação de responsabilidades.

---

## Conclusão

A combinação dos padrões **Factory Method**, **Facade** e **Observer** trouxe uma arquitetura mais limpa, flexível e escalável para o sistema imobiliário:

- O **Factory Method** resolveu o problema da criação dispersa e acoplada de objetos.
- O **Facade** centralizou a interface de acesso ao sistema, simplificando o uso pela interface gráfica.
- O **Observer** permitiu implementar notificações reativas de forma desacoplada e extensível.

O uso desses padrões está alinhado com os princípios SOLID e boas práticas de engenharia de software, preparando o sistema para futuras expansões e manutenções com menor custo.
