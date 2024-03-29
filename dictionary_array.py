# Degree Senpai 0.1 2023 by Alan Zhang, MIT Open Source License 

from collections import OrderedDict

class Dict_Array():

    def __init__(self, convert=None, list_type='list', ordered_dict=False):
        if ordered_dict:
            self.dictionary = OrderedDict()
        else:
            self.dictionary = dict()

        self.list_type = list_type

        if convert is not None:
            if isinstance(convert, dict):
                for key, value in convert.items():
                    self.add(key, value)


    def convert_list_type(self, list_type):
        for key, elements in self.dictionary.items():
            if list_type == 'list':
                self.dictionary.update({key:list(elements)})
            elif list_type == 'set':
                self.dictionary.update({key:set(elements)})
        self.list_type = list_type


    def prune(self, discriminator, remove_empty_keys=True) -> None:
        for _, elements in self.dictionary.items():
            remove_list = []
            for element in elements:
                if discriminator(element):
                    remove_list.append(element)
            for marked_element in remove_list:
                elements.remove(marked_element)
        if not remove_empty_keys:
            return
        
        remove_keys = set()
        for key, elements in self.dictionary.items():
            if not len(elements):
                remove_keys.add(key)

        for key in remove_keys:
            self.dictionary.pop(key)

    
    def collapse(self) -> dict:
        collapsed_dict = dict()
        for key, elements in self.dictionary.items():
            if len(elements) > 0:
                collapsed_dict.update({key:elements[0]})
            elif len(elements) > 1:
                print(f'WARNING IN DICT ARRAY COLLAPSE, KEY {key} HAS MORE THAN ONE ELEMENT IN ARRAY!')
        return collapsed_dict

    
    def sort(self) -> None:
        if self.list_type == 'list':
            for key, _ in self.dictionary.items():
                self.dictionary.get(key).sort()


    def insert(self, key, element, index) -> None:
        if self.list_type == 'list':
            self.dictionary.get(key).insert(index, element)
        else:
            self.add(key, element)


    def get(self, key, __default=None) -> None:
        return self.dictionary.get(key, __default)


    def add(self, key, element, overwrite=False) -> None:
        '''
        adds element to dict array by appending it to array of its cooresponding key
        '''
        if key in self.dictionary:
            if self.list_type == 'list':
                if overwrite:
                    self.dictionary.update({key:[element]})
                else:
                    self.dictionary.get(key).append(element)
            elif self.list_type == 'set':
                if overwrite:
                    self.dictionary.update({key:{element}})
                else:
                    self.dictionary.get(key).add(element)
        else:
            if self.list_type == 'list':
                self.dictionary.update({key:[element]})
            elif self.list_type == 'set':
                self.dictionary.update({key:{element}})


    def extend_elements(self, key, elements, overwrite=False) -> None:
        '''
        parameters:
            key: key of elements
            elements: iterable set to append to dictionary

        iterate over elements to add to values of its cooresponding keys in dictionary
        '''
        if not isinstance(elements, list) and not isinstance(elements, set):
            elements = [elements]
        if key in self.dictionary:
            if overwrite:
                self.dictionary.update({key:elements})
            elif self.list_type == 'list':
                self.dictionary.get(key).extend(elements)
            elif self.list_type == 'set':
                self.dictionary.get(key).update(elements)
        else:
            if self.list_type == 'list':
                self.dictionary.update({key:list(elements)})
            elif self.list_type == 'set':
                self.dictionary.update({key:set(elements)})


    def extend(self, other, overwrite=False):
        '''
        other (Dict_Array)

        merges two dict arrays together
        '''
        if isinstance(other, dict):
            for key, elements in other.items():
                self.extend_elements(key, elements, overwrite)
        else:
            for key, elements in other.dictionary.items():
                self.extend_elements(key, elements, overwrite)


    def remove(self, key, element=None, suppress_error=False) -> None:
        try:
            if key not in self.dictionary:
                if suppress_error:
                    return
                raise ValueError("key not found")
            
            if element is None:
                self.dictionary.pop(key)
            
            if self.list_type == 'list':
                if element not in self.dictionary.get(key) and suppress_error:
                    print('====ERROR SUPPRESSED IN DICT ARRAY REMOVE====')
                    return
                self.dictionary.get(key).remove(element)
            elif self.list_type == 'set':
                if element not in self.dictionary.get(key) and suppress_error:
                    print('====ERROR SUPPRESSED IN DICT ARRAY REMOVE====')
                    return
                self.dictionary.get(key).remove(element)

            if not len(self.dictionary.get(key)):
                self.pop(key)
                
        except ValueError as e:
            if suppress_error:
                return
            raise ValueError(e)


    def rename_key(self, old_key, new_key, suppress_error=False):
        if old_key not in self.dictionary:
            if suppress_error:
                return
            raise ValueError('key not found')
        elements = self.dictionary.get(old_key)
        self.dictionary.pop(old_key)
        self.dictionary.update({new_key:elements})


    def pop(self, key) -> list:
        return self.dictionary.pop(key, [])


    def replace(self, key, element) -> None:
        self.remove(key)
        self.add(key, element)


    def contains(self, key, element) -> bool:
        return element in self.dictionary.get(key, [])
    
    
    def to_tuples(self):
        return [[key, elements] for key,elements in self.dictionary.items()]
    

    def elements(self):
        elements = []
        for _ , e in self.dictionary.items():
            elements.extend(e)
        return elements
    

    def find_element(self, element):
        keys = []
        for key, elements in self.dictionary.items():
            if element in elements:
                keys.append(key)
        return keys
    

    def sort_elements(self, method_call=None, method_args:tuple=None, reverse=False):
        reverser = 1
        if reverse:
            reverser = -1
        for key, elements in self.dictionary.items():
            self.dictionary.update({key:sorted(elements, key = lambda x:reverser * getattr(x, method_call)(*method_args))})


    def items(self):
        return self.dictionary.items()


    def __len__(self):
        return len(self.dictionary)


    def __repr__(self):
        return str(self.dictionary)
    
    def __eq__(self, other):
        return self.dictionary == other.dictionary
    
    def __hash__(self):
        hashed = 0
        for key in self.dictionary.keys():
            hashed += hash(str(key))
        return hashed
