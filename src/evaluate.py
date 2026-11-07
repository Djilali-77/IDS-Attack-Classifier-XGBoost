from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

class ModelEvaluator:
    def __init__(self):
        pass

    def evaluate(self, y_true, y_pred, model_name="Model"):
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        
        print(f"Accuracy = {accuracy} \n Precision= {precision} \n Recall= {recall} \n F1= {f1}  \n\n")
    
    def get_confusion_matrix(self, y_true, y_pred):
        cm = confusion_matrix(y_true, y_pred)
        print(f"Confusion matrix = {cm} \n\n")
    
    def print_full_report(self, y_true, y_pred):
        cp = classification_report(y_true, y_pred)
        print(f"Full report = {cp} \n\n")