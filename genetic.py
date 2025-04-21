import random
from typing import List

## Meta, resolver a equação: a + 2b - 3c = 15
## Genes do genoma: a, b e c

##Parametros
lengthPopulation: int = 100
minValuePopulation: int = 1
maxValuePopulation: int = 20
goal: int = 15

rateMutation: float = 0.05
lowerMutation: int = 5
upperMutation: int = 15

## Classe do genoma
class Genome:
    def __init__(self, a, b, c, generation):
        self.a: int = a
        self.b: int = b
        self.c: int = c
        self.fitness: float = 0.0
        self.generation: int = generation

    def add_fitness(self, fitness):
        self.fitness = fitness

    def clear_fitness(self):
        self.fitness: float = 0.0

    def __repr__(self):
        return f"Genome(a={self.a}, b={self.b}, c={self.c}, generation={self.generation})"

##Atributos
before_best_genome : Genome = Genome(0,0,0,0)

## Função secundária para cálculo da equação
def calc(param: Genome) -> int:
    value_return : int = param.a + 2 * param.b - 3 * param.c
    return value_return

## Cria os genes aleatórios gerando o genoma e retorna uma lista para gerar a população inicial
def create_initial_population(size: int, lower: int, upper : int) -> List[Genome]:
    aux_population: List[Genome] = []

    for _ in range(size):
        aux_individual = Genome(random.randint(lower, upper),
                            random.randint(lower, upper),
                            random.randint(lower, upper),
                            1)

        aux_population.append(aux_individual)
    return aux_population

## Função para verificar quao perto está do objetivo
def fitness_function(param_individual: Genome) -> float:
    return 1 / (abs(calc(param_individual) - 15) + 1)

## Funcao de seleção, calcula o fitness,
def select (param_population) -> List[Genome]:
    length_population = len(param_population)
    quantity_limit_per_rollet: int = round(length_population / 2)
    new_population_auxiliary: List[Genome] = []

    ## Ordena com o maior fitness
    ordered_population = sorted(param_population, key=lambda x: x.fitness, reverse=True)

    ## Sorteia os indivíduos
    while len(new_population_auxiliary) < quantity_limit_per_rollet:
        # Recalcula os pesos com base no ranking atual
        weights = [len(ordered_population) - i for i in range(len(ordered_population))]
        total_weight = sum(weights)

        # Gira a roleta
        rollet = random.uniform(0, total_weight)
        accumulated = 0

        for j, individuo in enumerate(ordered_population):
            accumulated += weights[j]
            if accumulated >= rollet:
                new_population_auxiliary.append(individuo)

                # Remove o indivíduo da população para evitar seleção duplicada
                ordered_population.pop(j)
                break

    return new_population_auxiliary

## Funcao para juntar os pais e forma um filho, escolher os genes aleatorio.
def crossover(parent1 : Genome, parent2 : Genome, generate: int) -> (Genome, Genome) :
    return Genome(
        random.choice([parent1.a, parent2.a]),
        random.choice([parent1.b, parent2.b]),
        random.choice([parent1.c, parent2.c]),
        generate
    ), Genome(
        random.choice([parent1.a, parent2.a]),
        random.choice([parent1.b, parent2.b]),
        random.choice([parent1.c, parent2.c]),
        generate
    )

## Função para alterar o gene
def mutate_gene(gene: int) -> int:
    new_gene: int = gene

    if random.random() < 0.2: ## 20 % de ficar igual
        return new_gene
    elif random.random() < 0.6: ## 40 % de somar
        new_gene = gene + random.randint(lowerMutation, upperMutation)
        if new_gene > maxValuePopulation :
            new_gene = maxValuePopulation
    else: ## 40 % de diminuir
        new_gene = gene - random.randint(lowerMutation, upperMutation)
        if new_gene < minValuePopulation:
            new_gene = minValuePopulation

    return new_gene

## Função para verificar a mutação
def mutation(param_individual: Genome, generate: int) -> Genome:
    if random.random() > rateMutation:
        return param_individual

    a = mutate_gene(param_individual.a)
    b = mutate_gene(param_individual.b)
    c = mutate_gene(param_individual.c)

    return Genome(a, b, c, generate)

def termination_condition(population_actual: List[Genome], generation_actual: int) -> bool:
    population_actual.sort(key=lambda x: x.fitness, reverse=True)

    best_individual = population_actual[0]

    if best_individual.fitness == 1:
        print(best_individual)
        return True
    else:
        global before_best_genome

        if best_individual.fitness <= before_best_genome.fitness:
            diff_generation = generation_actual - before_best_genome.generation
            if diff_generation >= 10:
                print(f"Maximum of generations without progress, generation actual ${generation_actual}")
                return True
        else :
            before_best_genome = best_individual

        return False

if __name__ == '__main__':
    population : List[Genome] = create_initial_population(lengthPopulation, minValuePopulation, maxValuePopulation)
    generation = 1
    while True :
        for individual in population:
            individual.clear_fitness()
            individual.add_fitness(fitness_function(individual))

        if termination_condition(population, generation):
            break

        if generation > 100000:
            print("Max generation reached")
            break

        generation += 1

        new_population = select(population)
        for i in range(0, len(new_population), 2):
            try:
                child1, child2 = crossover(new_population[i], new_population[i + 1], generation)
                new_population.append(child1)
                new_population.append(child2)
            except IndexError:
                print("List index out of range")
                break

        for individual in new_population:
            individual = mutation(individual, generation)

        population = new_population
