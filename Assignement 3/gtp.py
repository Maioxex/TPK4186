import random

class Batch:
    def __init__(self, id, size, current_task):
        self.id = id
        self.size = size
        self.current_task = current_task

    def update_task(self, task):
        self.current_task = task

class Buffer:
    def __init__(self, id, max_capacity=120):
        self.id = id
        self.max_capacity = max_capacity
        self.stored_batches = []

    def load_batch(self, batch):
        if not self.is_full(batch.size):
            self.stored_batches.append(batch)
        else:
            raise Exception("Buffer is full!")

    def remove_batch(self, batch):
        self.stored_batches.remove(batch)

    def is_full(self, batch_size):
        return sum(batch.size for batch in self.stored_batches) + batch_size > self.max_capacity

    def get_next_batch(self):
        if self.stored_batches:
            return self.stored_batches.pop(0)
        else:
            return None

class Task:
    def __init__(self, id, processing_time_per_wafer):
        self.id = id
        self.processing_time_per_wafer = processing_time_per_wafer
        self.input_buffer = None
        self.output_buffer = None

    def set_buffers(self, input_buffer, output_buffer):
        self.input_buffer = input_buffer
        self.output_buffer = output_buffer

class Unit:
    def __init__(self, id, assigned_tasks=[]):
        self.id = id
        self.assigned_tasks = assigned_tasks
        self.current_batch = None
        self.state = "idle"

    def assign_tasks(self, tasks):
        self.assigned_tasks = tasks

    def load_batch(self, batch):
        if self.state == "idle":
            self.current_batch = batch
            self.state = "loaded"

    def unload_batch(self):
        if self.state == "processed":
            self.output_buffer.load_batch(self.current_batch)
            self.current_batch = None
            self.state = "idle"

    def process_batch(self):
        if self.state == "loaded":
            current_task = self.current_batch.current_task
            task_index = self.assigned_tasks.index(current_task)
            next_task_index = task_index + 1
            if next_task_index < len(self.assigned_tasks):
                next_task = self.assigned_tasks[next_task_index]
                task = self.production_line.tasks[next_task]
                processing_time = task.processing_time_per_wafer * self.current_batch.size
                self.current_batch.update_task(next_task)
                self.state = "processed"
                return processing_time
            else:
                # Last task completed
                self.state = "unloaded"
                return 0

    def select_next_batch(self):
        if self.state == "idle":
            self.load_batch()
            if self.current_batch is not None:
                current_task = self.current_batch.current_task
                next_task = current_task + 1 if current_task < len(self.assigned_tasks) - 1 else current_task
                task_index = self.assigned_tasks.index(self.assigned_tasks[next_task])
                processing_time = self.process_batch(task_index)
                self.unload_batch()
                return processing_time
            else:
                return 0

class ProductionLine:
    def __init__(self, units, tasks, buffers):
        self.units = units
        self.tasks = tasks
        self.buffers = buffers

    def process(self):
        total_time = 0
        processing = True

        while processing:
            unit_processing_times = []
            for unit in self.units:
                unit_processing_time = unit.select_next_batch()
                unit_processing_times.append(unit_processing_time)

            max_processing_time = max(unit_processing_times)
            total_time += max_processing_time + 2  # add loading and unloading time

            self.print_status()  # Observe the production process

            if all(time == 0 for time in unit_processing_times):
                processing = False

        return total_time

    def get_processing_time(self, task_id, batch_size):
        task = self.tasks[task_id]
        return task.get_processing_time(batch_size)

    def print_status(self):
        print("\nProduction Line Status:")
        for unit in self.units:
            print(f"Unit {unit.id}:")
            print(f"  State: {unit.state}")
            if unit.current_batch:
                print(f"  Current Batch: {unit.current_batch.id} (size: {unit.current_batch.size}, task: {unit.current_batch.current_task})")
            else:
                print(f"  Current Batch: None")

            print(f"  Input Buffer: {unit.input_buffer.id}")
            print(f"    Stored Batches: {[batch.id for batch in unit.input_buffer.load_batches]}")

            print(f"  Output Buffer: {unit.output_buffer.id}")
            print(f"    Stored Batches: {[batch.id for batch in unit.output_buffer.load_batches]}")


class Action:
    def __init__(self, action_type, buffer=None, unit=None, batch=None, task=None, start_time=0, end_time=0):
        self.action_type = action_type
        self.buffer = buffer
        self.unit = task.input_buffer if action_type == "load" else unit
        self.batch = batch
        self.task = task
        self.start_time = start_time
        self.end_time = end_time


    def is_ready(self, current_time):
        return self.start_time <= current_time

    def execute(self):
        if self.action_type == "load":
            self.unit.load_batch(self.batch)
        elif self.action_type == "process":
            self.unit.process_batch(self.task.id)
        elif self.action_type == "unload":
            self.unit.unload_batch(self.batch, self.task)


            
    def __str__(self):
        return f"{self.action_type.capitalize()} Batch {self.batch.id} at {'Buffer' if self.buffer else 'Unit'} {self.buffer.id if self.buffer else self.unit.id} (Task {self.task if self.task else '-'}) from {self.start_time} to {self.end_time}"
   
    def load_batches(self, batches, loading_times):
        next_task = 0  # initialize next_task as the first task
        for batch, loading_time in zip(batches, loading_times):
            unit = self.production_line.units[next_task]
            action = Action(
                action_type="load",
                unit=unit,
                buffer=unit.input_buffer,
                batch=batch,
                task=self.production_line.tasks[next_task],
                start_time=loading_time,
                end_time=loading_time + 1,
            )
            self.scheduler.add_action(action)
            next_task = (next_task + 1) % len(self.production_line.units)  # increment next_task in a circular fashion




class Scheduler:
    def __init__(self):
        self.actions = []

    def add_action(self, action):
        self.actions.append(action)
        self.sort_actions()

    def remove_action(self, action):
        self.actions.remove(action)

    def get_next_action(self):
        if self.actions:
            return self.actions.pop(0)
        else:
            return None

    def sort_actions(self):
        self.actions.sort(key=lambda x: x.end_time)


class Simulator:
    def __init__(self, production_line):
        self.production_line = production_line
        self.scheduler = Scheduler()

    def load_batches(self, batches, loading_times):
        for batch, loading_time in zip(batches, loading_times):
            action = Action(
                action_type="load",
                task=self.production_line.tasks[0],
                batch=batch,
                start_time=loading_time,
                end_time=loading_time + 1,
            )
            self.scheduler.add_action(action)


    def run_simulation(self, output_file=None):
        current_time = 0
        if output_file:
            file = open(output_file, "w")
        while True:
            action = self.scheduler.get_next_action()
            if action is None:
                break

            if action.is_ready(current_time):
                action.execute()
                current_time = action.end_time
                
                if output_file:
                    file.write(str(action) + "\n")
                
                # Schedule new actions
                if action.action_type == "load":
                    # Schedule processing action
                    next_task = action.batch.current_task
                    print("next_task:", next_task)
                    unit = self.production_line.units[next_task]
                    processing_time = self.production_line.get_processing_time(next_task, action.batch.size)
                    process_action = Action("process", action.unit, action.batch, action.task, current_time, current_time + processing_time)
                    self.scheduler.add_action(process_action)
                elif action.action_type == "unload":
                    # Schedule loading the next task
                    if action.batch.current_task < len(self.production_line.tasks) - 1:
                        next_task = action.batch.current_task + 1
                        unit = self.production_line.units[next_task]
                        load_action = Action("load", unit, action.batch, next_task, current_time, current_time + 1)
                        self.scheduler.add_action(load_action)
            else:
                self.scheduler.add_action(action)  # Add the action back to the scheduler
                current_time += 1
        if output_file:
            file.close()
        
        return current_time




# Create tasks
tasks = [Task(i, processing_time) for i, processing_time in enumerate([0.5, 3.5, 1.2, 3, 0.8, 0.5, 1, 1.9, 0.3])]

# Create units
unit1 = Unit(0, [tasks[0], tasks[2], tasks[5], tasks[8]])
unit2 = Unit(1, [tasks[1], tasks[4], tasks[6]])
unit3 = Unit(2, [tasks[3], tasks[7]])

# Create buffers
buffers = [Buffer(i) for i in range(len(tasks))]

# Assign input/output buffers to tasks
for i, task in enumerate(tasks):
    task.set_buffers(buffers[i], buffers[i])

# Create production line
production_line = ProductionLine([unit1, unit2, unit3], tasks, buffers)

# Create simulator
simulator = Simulator(production_line)

# Create batches
batches = [Batch(i, random.randint(20, 50), 0) for i in range(20)]  # Adjust the number of batches to produce 1000 wafers

# Assign tasks to batches
for batch in batches:
    batch.update_task(tasks)

# Load batches into the input buffer of the production line
simulator.load_batches(batches, [i for i in range(len(batches))])  # Adjust the loading times as needed

# Run simulation and print actions to a text file
simulator.run_simulation(output_file="simulation_trace.txt")

# Create one batch of size 50
batches = [Batch(0, 50, 0)]

# Assign tasks to the batch
batches[0].update_task(tasks)
# Create a few batches with different sizes
batches = [Batch(i, size, 0) for i, size in enumerate([25, 30, 40])]


# Assign tasks to the batches
for batch in batches:
    batch.update_task(tasks)
# Create batches with varying sizes to produce 1000 wafers
batches = [Batch(i, size, 0) for i, size in enumerate([30, 40, 25, 45, 20, 50, 30, 50, 45, 20, 35, 25, 40, 20, 35, 30, 50, 40, 25, 30])]

# Assign tasks to the batches
for batch in batches:
    batch.update_task(tasks)
simulator.load_batches(batches, [i for i in range(len(batches))])  # Adjust the loading times as needed

# Run simulation and print actions to a text file
simulator.run_simulation(output_file="simulation_trace.txt")