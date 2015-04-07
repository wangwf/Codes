
def _splitList(head):
    fast = head
    slow = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    middle = slow.next
    slow.next = None
    return head, middle

def _reversedList(head):
    prev = None
    curr = head

    while curr:
        temp = curr.next
        curr.next = prev
        prev= curr
        curr= temp

    return prev


def _mergeLists(a, b):

    head = a
    tail = a

    a = a.next
    while b:
        tail.next = b
        tail = tail.next
        b = b.next
        if a:
            a, b = b, a

    return head

def reorderList(head):
    if not head or not head.next:
        return

    a, b = _splitList(head)
    b = _reverseList(b)

    head = _mergeLists(a, b)

