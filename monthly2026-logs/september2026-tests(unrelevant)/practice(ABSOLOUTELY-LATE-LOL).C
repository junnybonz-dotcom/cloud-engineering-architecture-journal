#include <stdio.h>

int main() {

    int pin;
    int correctPin = 1234;
    int choice;
    int quantity;
    int action;
    float price;
    float total = 0;

    // PIN LOGIN
    do {
        printf("\nEnter PIN: ");
        scanf("%d", &pin);

        if (pin != correctPin) {
            printf("Incorrect PIN. Try again.\n");
        }

    } while (pin != correctPin);

    printf("\nPIN accepted!\n");

    // MENU LOOP
    do {

        printf("\n===== MENU =====\n");
        printf("1. Water  - P20\n");
        printf("2. Chips  - P35\n");
        printf("3. Soda   - P30\n");
        printf("4. Coffee - P40\n");
        printf("5. Fruits - P50\n");
        printf("6. Exit\n");

        printf("Choose a product: ");
        scanf("%d", &choice);

        // SELECT PRODUCT
        switch (choice) {

            case 1:
                price = 20;
                printf("You selected Water.\n");
                break;

            case 2:
                price = 35;
                printf("You selected Chips.\n");
                break;

            case 3:
                price = 30;
                printf("You selected Soda.\n");
                break;

            case 4:
                price = 40;
                printf("You selected Coffee.\n");
                break;

            case 5:
                price = 50;
                printf("You selected Fruits.\n");
                break;

            case 6:
                printf("Thank you!\n");
                return 0;

            default:
                printf("Invalid choice.\n");
                continue;
        }

        // QUANTITY
        printf("Enter quantity: ");
        scanf("%d", &quantity);

        total = total + (price * quantity);

        printf("Added to cart!\n");
        printf("Current total: P%.2f\n", total);

        // ACTION
        printf("\nWhat would you like to do?\n");
        printf("1. Add to cart / Continue shopping\n");
        printf("2. Continue to payment\n");
        printf("3. Exit\n");

        printf("Choose: ");
        scanf("%d", &action);

        if (action == 2) {

            printf("\n===== PAYMENT =====\n");
            printf("Total amount: P%.2f\n", total);
            printf("Payment successful!\n");
            printf("Thank you for your purchase!\n");

            break;

        } else if (action == 3) {

            printf("\nThank you! Goodbye.\n");
            break;

        } else if (action != 1) {

            printf("Invalid action.\n");
        }

    } while (1);

    return 0;
}

