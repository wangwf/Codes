class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

    def rotateRight(self, head, k):
        if head== None or head.next ==None or k ==0:
            return head

        curr = head
        while k>0:
            curr = curr.next
            k -=1
            if curr==None: curr=head
        if curr == head:
            return head

        p = head
        while curr.next != None:
            p = p.next
            curr = curr.next

        newHead = p.next
        p.next = None
        curr.next = head

        return newHead
