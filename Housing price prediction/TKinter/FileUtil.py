# FileUtil.py [cite: 353]
import pickle

class FileUtil:
    @staticmethod
    def savemodel(model, filename):
        try:
            # Lưu mô hình ra file nhị phân [cite: 353]
            pickle.dump(model, open(filename, 'wb'))
            return True
        except:
            print("An exception occurred")
            return False

    # FileUtil.py [cite: 353]
    import pickle

    class FileUtil:
        @staticmethod
        def savemodel(model, filename):
            try:
                # Lưu mô hình ra file nhị phân [cite: 353]
                pickle.dump(model, open(filename, 'wb'))
                return True
            except:
                print("An exception occurred")
                return False

        @staticmethod
        def loadmodel(filename):
            try:
                # Tải mô hình từ file nhị phân [cite: 353]
                model = pickle.load(open(filename, 'rb'))
                return model
            except:
                print("An exception occurred")
                return None
    @staticmethod
    def loadmodel(filename):
        try:
            # Tải mô hình từ file nhị phân [cite: 353]
            model = pickle.load(open(filename, 'rb'))
            return model
        except:
            print("An exception occurred")
            return None