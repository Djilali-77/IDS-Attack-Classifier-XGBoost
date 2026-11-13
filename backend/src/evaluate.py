from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

class ModelEvaluator:
    def evaluate(self, y_true, y_pred):
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        f1_weighted = f1_score(y_true, y_pred, average='weighted')
        # Macro F1 treats every class the same, so rare attacks count as much as BENIGN
        f1_macro = f1_score(y_true, y_pred, average='macro')

        print(f"Accuracy = {accuracy}")
        print(f"Precision (weighted) = {precision}")
        print(f"Recall (weighted) = {recall}")
        print(f"F1 (weighted) = {f1_weighted}")
        print(f"F1 (macro) = {f1_macro}\n")

    def get_confusion_matrix(self, y_true, y_pred):
        cm = confusion_matrix(y_true, y_pred)
        print(f"Confusion matrix =\n{cm}\n")

    def print_full_report(self, y_true, y_pred, class_names=None):
        # Passing labels makes sure every class shows up, even if it was never predicted
        labels = range(len(class_names)) if class_names is not None else None
        report = classification_report(
            y_true, y_pred, labels=labels, target_names=class_names, zero_division=0
        )
        print(f"Full report =\n{report}\n")