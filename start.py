from computations import get_raw_dictionary, get_indexes, get_all_metrics, get_beta_f_measure_dependency
from db_communication import send_metrics_to_db, send_f_measure_dependency
from web import send_notification, import_data
import time
import gc
from datetime import datetime, date


def main():
    if 1 == 1:
        send_notification("Этот текст появится в уведомлении")

    timing = time.time()
    while True:
        if time.time() - timing > 3.0:  # Время задержки выполнения скрипта, в секундах

            timestamp = datetime.now()
            indexes = get_indexes(get_raw_dictionary(import_data(timestamp)))
            metrics = get_all_metrics(indexes, 1)

            send_metrics_to_db(indexes, metrics, timestamp)

            timing = time.time()
            del timestamp, indexes, metrics
            gc.collect()


if __name__ == '__main__':
    main()
