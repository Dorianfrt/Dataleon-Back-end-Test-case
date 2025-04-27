#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node* next;
} Node;

Node* create_node(int data) {
    Node* new_node = malloc(sizeof(Node));
    if (!new_node) {
        perror("malloc failed");
        return NULL;
    }
    new_node->data = data;
    new_node->next = NULL;
    return new_node;
}

void append(Node** head, int data) {
    Node* new_node = create_node(data);
    if (!new_node)
        return;
    if (*head == NULL) {
        *head = new_node;
    } else {
        Node* temp = *head;
        while (temp->next != NULL)
            temp = temp->next;
        temp->next = new_node;
    }
}

void print_list(Node* head) {
    Node* temp = head;
    while (temp != NULL) {
        printf("%d -> ", temp->data);
        temp = temp->next;
    }
    printf("NULL\n");
}

void free_list(Node* head) {
    Node* temp;
    while (head != NULL) {
        temp = head;
        head = head->next;
        free(temp);
    }
}

int main() {
    Node* head = NULL;

    append(&head, 10);
    append(&head, 20);
    append(&head, 30);

    printf("Liste chaînée : ");
    print_list(head);

    free_list(head);
    return 0;
}
