import csv
from major import getCourseContentHandler, getUrlsHandler, dynamicMaxLimit

try:

    success_limit, limit_value = dynamicMaxLimit()

    if success_limit:
        urls = getUrlsHandler(limit_value)

        if urls:
            success_content, data_array = getCourseContentHandler(urls)

            if success_content and isinstance(data_array, list):
                with open('majorCourses.csv', 'w', newline='') as csvfile:
                    fieldnames = data_array[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in data_array:
                        writer.writerow(row)
            else:
                print("No content to write to CSV.")
        else:
            print("Failed to obtain URLs.")
    else:
        print("Failed to obtain limit.")

except Exception as e:
    print("An exception occurred:", str(e))

