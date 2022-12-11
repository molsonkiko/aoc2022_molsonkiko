package deque

import "fmt"

type Node struct {
	Left  *Node
	Right *Node
	Value interface{}
}

type Deque struct {
	Left   *Node
	Right  *Node
	Length int
}

func NewDeque() Deque {
	return Deque{nil, nil, 0}
}

func (dq *Deque) AddRight(value interface{}) {
	right := dq.Right
	node := Node{right, nil, value}
	if right == nil {
		dq.Left = &node
	}
	dq.Right = &node
	dq.Length++
}

func (dq *Deque) AddLeft(value interface{}) {
	left := dq.Left
	node := Node{nil, left, value}
	if left == nil {
		dq.Right = &node
	}
	dq.Left = &node
	dq.Length++
}

func (dq *Deque) PopLeft() (value interface{}, err error) {
	if dq.Length == 0 {
		return nil, fmt.Errorf("can't pop from a deque of length 0")
	}
	val := dq.Left.Value
	dq.Left.Right = nil
	if dq.Length == 1 {
		dq.Right = nil
	}
	dq.Left = nil
	dq.Length--
	return val, nil
}

func (dq *Deque) PopRight() (value interface{}, err error) {
	if dq.Length == 0 {
		return nil, fmt.Errorf("can't pop from a deque of length 0")
	}
	dq.Right.Left = nil
	val := dq.Right.Value
	if dq.Length == 1 {
		dq.Left = nil
	}
	dq.Right = nil
	dq.Length--
	return val, nil
}

func (dq *Deque) GetLeft() (value interface{}, err error) {
	if dq.Length == 0 {
		return nil, fmt.Errorf("can't get left value of deque of length 0")
	}
	return dq.Left.Value, nil
}

func (dq *Deque) GetRight() (value interface{}, err error) {
	if dq.Length == 0 {
		return nil, fmt.Errorf("can't get right value of deque of length 0")
	}
	return dq.Right.Value, nil
}
