import sys

def save_evento_futebol(partida,golos_casa,golos_visitante):
    with open('rasbet/eventoslog','a') as f:
      f.write('futebol/'+partida+'/'+golos_casa+'/'+golos_visitante+'/\n')




def save_evento_formula1(partida,vencedor):
    with open('rasbet/eventoslog','a') as f:
      f.write('formula1/'+partida+'/'+vencedor+'/\n')

def main():
    argc=len(sys.argv)
    if  argc< 2:
        print("Not a valid event")
    else:
        if sys.argv[1]=="futebol":
            if argc < 5:
                print("Not a valid football event")
            else:
                partida=sys.argv[2]
                golos_casa=sys.argv[3]
                golos_visitante=sys.argv[4]
                save_evento_futebol(partida,golos_casa,golos_visitante)
        elif sys.argv[1]=="formula1":
            if argc < 4:
                print("Not a valid formula1 event")
            else:
                partida=sys.argv[2]
                vencedor=sys.argv[3]
                save_evento_formula1(partida,vencedor)

  
  
if __name__=="__main__":
    main()
