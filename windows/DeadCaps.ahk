﻿;;; DeadCaps for AutoHotKey / Windows 20.02

Suspend,On

CapsLock::
    Suspend, Off
    If(GetKeyState("CapsLock", "T")){
	SetCapsLockState, Off
	Suspend, On
	return
    }
    If(A_PriorKey="CapsLock"){
	SetCapsLockState, On
	Suspend, On
	return
    }
    return

a::
    Send,A
    Suspend,On
    return
b::
    Send,B
    Suspend,On
    return
c::
    Send,C
    Suspend,On
    return
d::
    Send,D
    Suspend,On
    return
e::
    Send,E
    Suspend,On
    return
f::
    Send,F
    Suspend,On
    return
g::
    Send,G
    Suspend,On
    return
h::
    Send,H
    Suspend,On
    return
i::
    Send,I
    Suspend,On
    return
j::
    Send,J
    Suspend,On
    return
k::
    Send,K
    Suspend,On
    return
l::
    Send,L
    Suspend,On
    return
m::
    Send,M
    Suspend,On
    return
n::
    Send,N
    Suspend,On
    return
o::
    Send,O
    Suspend,On
    return
p::
    Send,P
    Suspend,On
    return
q::
    Send,Q
    Suspend,On
    return
r::
    Send,R
    Suspend,On
    return
s::
    Send,S
    Suspend,On
    return
t::
    Send,T
    Suspend,On
    return
u::
    Send,U
    Suspend,On
    return
v::
    Send,V
    Suspend,On
    return
w::
    Send,W
    Suspend,On
    return
x::
    Send,X
    Suspend,On
    return
y::
    Send,Y
    Suspend,On
    return
z::
    Send,Z
    Suspend,On
    return
,::
    Send,;
    Suspend,On
    return
.::
    Send,:
    Suspend,On
    return
-::
    Send,_
    Suspend,On
    return