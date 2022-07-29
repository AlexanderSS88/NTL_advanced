nested_list = [['a', 'b', 'c'], ['d', 'e', 'f', 'h', False], [1, 2, None]]
super_nested_list = [
	['a', 'b', 'c'], ['d', 'e', [77, 7.94, 'honda', [None, True, 'Nurdin', [5, 6.789, 'Jack', ['bagapsh', 1], 999]]], 'f', 'h', False], [1, 2, None]]
print('*' * 111)


"""exercise 1"""
class FlatIterator:

	def __init__(self, nested_list: list):
		self.nested_list = nested_list#

	def __iter__(self):
		self.cursor = 0
		self.nested_cursor = 0
		return self#

	def __next__(self):
		if self.nested_cursor < len(self.nested_list[self.cursor]) and self.nested_cursor != 0:
			position = self.nested_list[self.cursor][self.nested_cursor]
			self.nested_cursor += 1
			return position
		elif self.nested_cursor == 0 and self.cursor == 0:
			position = self.nested_list[self.cursor][self.nested_cursor]
			self.nested_cursor += 1
			return position
		elif self.nested_cursor == len(self.nested_list[self.cursor]) and self.cursor + 1 != len(self.nested_list):
			self.nested_cursor = 0
			self.cursor += 1
			position = self.nested_list[self.cursor][self.nested_cursor]
			self.nested_cursor += 1
			return position
		else:
			raise StopIteration

flat_list = [item for item in FlatIterator(nested_list)]
print(flat_list)

for item in FlatIterator(nested_list):
	print(item)
print('*' * 111)


"""exercise 2"""
def flat_generator(self):
	for id, simple_list in enumerate(nested_list):
		for item in simple_list:
			yield item
		if id + 1 > len(nested_list):
			raise StopIteration

for item in flat_generator(nested_list):
	print(item)

flat_list = ([item for item in flat_generator(nested_list)])
print(flat_list)
print('*' * 111)


"""exercise 3"""
class FlatIteratorUnlim:

	def __init__(self, super_nested_list: list):
		self.super_nested_list = super_nested_list

	def __iter__(self):
		self.cursor = 0
		self.nested_cursor = 0
		return self

	def __next__(self):
		self.nested_list = []
		while self.cursor < len(self.super_nested_list):
			# print(f"Курсор: {self.cursor} {self.nested_cursor} >>>> {self.super_nested_list}")
			if type(self.super_nested_list[self.cursor]) != list:
				position = self.super_nested_list[self.cursor]
				if self.cursor + 1 == len(self.super_nested_list):
					self.cursor += 1
					self.nested_cursor = 0
				else:
					self.cursor += 1
				return position
			elif type(self.super_nested_list[self.cursor]) == list and \
					type(self.super_nested_list[self.cursor][self.nested_cursor]) != list:
				if self.nested_cursor < len(self.super_nested_list[self.cursor]):
					position = self.super_nested_list[self.cursor][self.nested_cursor]
					if self.nested_cursor + 1 == len(self.super_nested_list[self.cursor]):
						self.nested_cursor = 0
						self.cursor += 1
					else:
						self.nested_cursor += 1
					return position
			elif type(self.super_nested_list[self.cursor]) == list and \
					type(self.super_nested_list[self.cursor][self.nested_cursor]) == list:
				nested_iterator = FlatIteratorUnlim(self.super_nested_list[self.cursor][self.nested_cursor])
				for item in nested_iterator:
					if self.cursor == len(self.super_nested_list):
						break
					# print(f"PRINT >>> {item}")
					self.nested_list.append(item)
				# print(f"NESTED >>>>{item}")
				self.nested_cursor = 0
				self.cursor += 1
				return self.nested_list
		raise StopIteration

for item in FlatIteratorUnlim(super_nested_list):
	print(item)

flat_list = [item for item in FlatIteratorUnlim(super_nested_list)]
print(flat_list)
print('*' * 111)


class FlatIterator_brain:

    def __init__(self, multi_list):
        self.multi_list = multi_list

    def __iter__(self):
        self.iterators_stack = [iter(self.multi_list)]  # стэк итераторов
        return self

    def __next__(self):
        while self.iterators_stack:  # пока в стеке есть итераторы
            try:
                current_element = next(self.iterators_stack[-1])
                #  пытаемся получить следующий элемент
            except StopIteration:
                self.iterators_stack.pop()
                continue
            if isinstance(current_element, list):
                # если следующий элемент оказался списком, то
                # добавляем его итератор в стек
                self.iterators_stack.append(iter(current_element))
            else:
                # если элемент не список, то просто возвращаем его
                return current_element
        raise StopIteration

for item in FlatIterator_brain(super_nested_list):
	print(item)

flat_list = [item for item in FlatIterator_brain(super_nested_list)]
print(flat_list)
print('*' * 111)


"""exercise 4"""
def flat_generator_unlim(super_nested_list):
    for i in super_nested_list:
        if isinstance(i, list):
            for j in flat_generator_unlim(i):
                yield j
        else:
            yield i

for item in flat_generator_unlim(super_nested_list):
	print(item)

flat_list = ([item for item in flat_generator_unlim(super_nested_list)])
print(flat_list)
