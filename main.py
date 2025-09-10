from src import data_processing, ml_model, report_generator

def main():
    data_processing.main()
    ml_model.run()
    report_generator.run()

if __name__ == "__main__":
    main()
