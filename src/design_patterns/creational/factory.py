"""
This module demonstrates the Factory design pattern, which is a creational pattern
used to create objects without specifying the exact class of object that will be created.
The Factory pattern defines an interface for creating an object, but allows subclasses 
to alter the type of objects that will be created. In this implementation, the 
AnimalFactory class creates instances of Dog or Cat based on the input type.
"""

from ..structural.inheritance import Animal, Dog, Cat

class AnimalFactory:
    """Factory class to create Animal instances.

    Usage:
        ```
        factory = AnimalFactory()
        dog = factory.get_animal("dog", "Buddy")
        print(dog.speak())  # Output: Buddy says woof!
        ```
    """

    def get_animal(self, animal_type: str, name: str) -> Animal:
        """Creates an instance of Animal based on the provided type.

        Args:
            animal_type (str): The type of animal to create ('dog' or 'cat').
            name (str): The name of the animal.

        Returns:
            Animal: An instance of Dog or Cat if the type is valid; None otherwise.
        """
        if animal_type == "dog":
            return Dog(name)
        elif animal_type == "cat":
            return Cat(name)
        else:
            return None
