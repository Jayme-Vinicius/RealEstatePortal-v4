# Implementação do Padrão Factory Method no Sistema Imobiliário

## Introdução

Este documento explica a implementação do padrão de projeto Factory Method no sistema de gerenciamento imobiliário. O Factory Method é um padrão criacional que fornece uma interface para criar objetos em uma superclasse, mas permite que as subclasses alterem o tipo de objetos que serão criados.

## Por que escolhemos o Factory Method?

### Problema inicial

O sistema imobiliário original criava objetos `Property` diretamente no código do controlador e na interface do usuário:

```python
new_property = Property(
    id=None,
    title=title,
    description=description,
    price=price,
    location=location,
    property_category=property_category,  # Casa, Apartamento ou Terreno
    transaction_type=transaction_type,
    agent=logged_user
)
```

Isso apresentava algumas desvantagens:

1. **Acoplamento forte**: O código cliente estava diretamente ligado à classe concreta `Property`
2. **Dificuldade de extensão**: Para adicionar novos tipos de propriedades, seria necessário modificar o código em vários lugares
3. **Lógica de criação dispersa**: A lógica para construir os diferentes tipos de propriedades estava espalhada pelo código

### Solução com Factory Method

O Factory Method resolve esses problemas ao:

1. **Encapsular a criação de objetos**: A lógica de criação é movida para classes específicas
2. **Fornecer extensibilidade**: Novos tipos de propriedades podem ser adicionados sem modificar o código existente
3. **Centralizar a lógica de criação**: Cada tipo de propriedade tem seu próprio criador específico

## Implementação no Sistema Imobiliário

A implementação consiste em três componentes principais:

### 1. Interface PropertyCreator

```python
class PropertyCreator(ABC):
    @abstractmethod
    def create_property(self, property_id, title, description, price, location, transaction_type, agent, virtual_tour_url=None):
        pass
```

Esta interface abstrata define o método que todos os criadores concretos devem implementar.

### 2. Criadores Concretos

Classes específicas para cada tipo de propriedade:

```python
class HouseCreator(PropertyCreator):
    def create_property(self, property_id, title, description, price, location, transaction_type, agent, virtual_tour_url=None):
        from property import Property
        return Property(
            id=property_id,
            title=title,
            description=description,
            price=price,
            location=location,
            property_category="Casa",
            transaction_type=transaction_type,
            agent=agent,
            virtual_tour_url=virtual_tour_url
        )
```

Classes semelhantes foram criadas para `ApartmentCreator` e `LandCreator`.

### 3. Fábrica Central

```python
class PropertyFactory:
    @staticmethod
    def get_property_creator(property_type):
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
        creator = PropertyFactory.get_property_creator(property_type)
        return creator.create_property(property_id, title, description, price, location, transaction_type, agent, virtual_tour_url)
```

Esta classe atua como ponto central para criar propriedades, selecionando o criador apropriado com base no tipo solicitado.

## Funcionamento no Código

O processo de criação de uma propriedade usando o Factory Method funciona da seguinte forma:

1. O controlador recebe uma solicitação para criar uma nova propriedade com um tipo específico
2. O controlador chama o método `create_property` da `PropertyFactory`, passando o tipo e os parâmetros necessários
3. A fábrica seleciona o criador adequado com base no tipo de propriedade
4. O criador instancia e retorna o objeto `Property` com a categoria específica
5. O controlador adiciona a propriedade ao sistema

Isso é evidenciado no método adicionado ao `PropertyController`:

```python
def create_property(self, property_type, title, description, price, location, transaction_type, agent, virtual_tour_url=None):
    property = PropertyFactory.create_property(
        property_type=property_type,
        property_id=None,
        title=title,
        description=description,
        price=price,
        location=location,
        transaction_type=transaction_type,
        agent=agent,
        virtual_tour_url=virtual_tour_url
    )
    
    return self.add_property(property)
```

## Benefícios Alcançados

A implementação do Factory Method trouxe diversos benefícios ao sistema:

1. **Baixo acoplamento**: O código cliente agora depende de interfaces abstratas em vez de classes concretas
2. **Princípio Open/Closed**: O sistema está aberto para extensão, mas fechado para modificação
3. **Encapsulamento**: A lógica de criação de cada tipo de propriedade está isolada em sua própria classe
4. **Manutenibilidade**: Alterações na construção de propriedades afetam apenas os criadores específicos
5. **Facilidade de testes**: Os criadores podem ser facilmente substituídos por mocks para testes unitários

## Extensibilidade Futura

Para adicionar um novo tipo de propriedade (por exemplo, "Comercial"), basta:

1. Criar uma nova classe `CommercialCreator` que implemente a interface `PropertyCreator`
2. Adicionar o novo tipo ao dicionário na `PropertyFactory`

O restante do sistema continuará funcionando sem modificações.

## Conclusão

O padrão Factory Method forneceu uma solução elegante para a criação de diferentes tipos de propriedades no sistema imobiliário. Ele melhorou a estrutura do código, reduzindo o acoplamento e aumentando a coesão, além de preparar o sistema para futuras expansões sem necessidade de modificações extensivas.
