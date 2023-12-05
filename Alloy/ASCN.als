sig Cliente{
	connection : one ReverseProxy_and_BalanceLoader
}

sig RasBet{
	db : one Coordinator
}

sig Coordinator{
	node : some DataNode
}

sig DataNode{}

sig GTM{
	coordinator : some Coordinator
}

one sig ReverseProxy_and_BalanceLoader{
	proxy_servers : some RasBet
}

fact {no c : Coordinator | c not in GTM.coordinator or c not in RasBet.db}

fact {no d : DataNode | d not in Coordinator.node}

fact {all w : RasBet, rp : ReverseProxy_and_BalanceLoader | w in rp.proxy_servers}

fact {all w: RasBet, c : Coordinator | c in w.db => #c = 1}

fact {
	one GTM
	one ReverseProxy_and_BalanceLoader
	some Cliente
	#Coordinator > 2
	#Coordinator < #DataNode + 2
	#Coordinator <= #RasBet
}

pred example {
	Coordinator = RasBet.db
}

run example for 15
