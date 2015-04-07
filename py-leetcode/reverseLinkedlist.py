
def reverseBetween(head, m, n):
    if m==n:
        return head

    dummyNode = ListNode(0)
    dummyNode.next = head
    newHead = dummyNode

    for i in range(m-1):
        newHead = newHead.next

    #reverse the [m, n] nodes
    pre = None
    cur = newHead.next

    for i in range(n-m+1):
        temp = cur.next
        cur.next = pre
        pre = cur
        cur = temp

    newHead.next.next = cur
    newHead.next = pre

    return dummyNode.next
