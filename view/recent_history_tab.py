# recent_history_tab.py
from tkinter import ttk

class RecentHistoryTab:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.tree = self.create_history_tree()

    def create_history_tree(self):
        # Create the Treeview widget for displaying history
        columns = ('Name', 'Gender', 'Probability', 'Date')
        tree = ttk.Treeview(self.parent, columns=columns, show='headings')

        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')

        # Place the tree in the parent widget
        tree.pack(expand=True, fill='both')

        return tree

    def update_history_tree(self, session_history):
        # Clear the tree before inserting new data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert each item in session_history into the tree
        for entry in session_history:
            self.tree.insert('', 'end', values=entry)

    def clear_history_tree(self):
        # Clear the tree when history is cleared
        for item in self.tree.get_children():
            self.tree.delete(item)
