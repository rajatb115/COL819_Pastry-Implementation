
import sys
from util import hashValue,int_val, common_len, update_table, randomGenerator, smallest_dis, randomGenerator2, str_value, sort_nodes, hex_dif


class Pastry_Node:
    tot_nodes=0
    #tot_data_ele=0
    tot_search_q=0
    tot_node_add=0
    #tot_data_add=0
    no_of_hope =0
    def __init__(self,node_id,x_axis,y_axis,all_nodes,d_closest_node=None):
        
        
        
        # Increasing the number of nodes in the network
        Pastry_Node.tot_nodes+=1
        
        # Increasing the number of nodes added in the network
        Pastry_Node.tot_node_add+=1
        
        # Store self node Id
        self.node_id = node_id
        
        # Storing the physical location of the node
        self.x_axis = x_axis
        self.y_axis = y_axis
        
        # Stores the left leaf nodes for the current node
        self.left_leaf = []
        
        # Stores the right leaf nodes for the current node
        self.right_leaf = []
        
        # Stores the least distant node from the current node
        self.neighbour_node = []
        
        # Creating an empty routing table (pow(2,b) * m)
        self.routing_table = []
        
        # Data elements
        self.data_element = []
        
        # Initializing the routing table
        for i in range(32):
            self.routing_table.append([None for j in range(16)])
        
        # If we have a node closer to current node, then we will find
        # the closest node to the current node numerically and fill the
        # details of the node
        hash_val = hashValue(self.node_id)
        for i in range(32):
            if(hash_val[i] in ['0','1','2','3','4','5','6','7','8','9']):
                self.routing_table[i][int(hash_val[i])] = self
            else:
                j = ord(hash_val[i])-ord('a')+10
                self.routing_table[i][j] = self
        
        
        if d_closest_node != None:
            self.join(d_closest_node,all_nodes)
        
    def add_element(self,ele):
        self.data_element.append(ele)
    
    def routing(self,s_closest_node,temp,all_nodes):
        
        if temp == "add":
            self.intermediate_node.append(s_closest_node)
            
        
        # If current node_id the final node
        if hashValue(s_closest_node.node_id) == hashValue(self.node_id):
            return s_closest_node
        
        # If the node is in range of leaf node
        elif len(s_closest_node.left_leaf)!=0 and len(s_closest_node.right_leaf)!=0 and  hashValue(s_closest_node.right_leaf[0].node_id) <= hashValue(self.node_id) and hashValue(s_closest_node.left_leaf[-1].node_id) >= hashValue(self.node_id) :
            
            #closest_id = hashValue(s_closest_node.node_id)
            closest_id = hex_dif (hashValue(self.node_id),hashValue(s_closest_node.node_id))
            closest_node = s_closest_node
            
            for node in s_closest_node.left_leaf:
                
                
                if closest_id >= hex_dif (hashValue(self.node_id),hashValue(node.node_id)):
                    closest_id = hex_dif (hashValue(self.node_id),hashValue(node.node_id))
                    closest_node = node
                
            for node in s_closest_node.right_leaf:
                if closest_id >= hex_dif (hashValue(self.node_id),hashValue(node.node_id)):
                    closest_id = hex_dif (hashValue(self.node_id),hashValue(node.node_id))
                    closest_node = node
            
            if temp == "add":
                self.intermediate_node.append(closest_node)
                return closest_node
        
        elif len(s_closest_node.left_leaf)!=0 and len(s_closest_node.right_leaf)==0 and  hashValue(s_closest_node.left_leaf[0].node_id) <= hashValue(self.node_id) and hashValue(s_closest_node.left_leaf[-1].node_id) >= hashValue(self.node_id) :
            
            closest_id = hex_dif (hashValue(self.node_id),hashValue(s_closest_node.node_id))
            closest_node = s_closest_node
            
            for node in s_closest_node.left_leaf:
                if closest_id > hex_dif (hashValue(self.node_id),hashValue(node.node_id)):
                    closest_id = hex_dif (hashValue(self.node_id),hashValue(node.node_id))
                    closest_node = node
                
            if temp == "add":
                self.intermediate_node.append(closest_node)
                return closest_node
            
        elif len(s_closest_node.left_leaf)==0 and len(s_closest_node.right_leaf)!=0 and  hashValue(s_closest_node.right_leaf[0].node_id) <= hashValue(self.node_id) and hashValue(s_closest_node.right_leaf[-1].node_id) >= hashValue(self.node_id) :
            
            closest_id = hex_dif (hashValue(self.node_id),hashValue(s_closest_node.node_id))
            closest_node = s_closest_node
            
            for node in s_closest_node.right_leaf:
                if closest_id > hex_dif (hashValue(self.node_id),hashValue(node.node_id)):
                    closest_id = hex_dif (hashValue(self.node_id),hashValue(node.node_id))
                    closest_node = node
        
            if temp == "add":
                self.intermediate_node.append(closest_node)
                return closest_node
    
        else:
            l = 0
            v1 = hashValue(s_closest_node.node_id)
            v2 = hashValue(self.node_id)
            
            for i in range(32):
                if(v1[i]==v2[i]):
                    l+=1
                else:
                    break
            
            if(s_closest_node.routing_table[l][int_val(v2[l])] != None):
                if (s_closest_node.routing_table[l][int_val(v2[l])] in self.intermediate_node):
                    return s_closest_node.routing_table[l][int_val(v2[l])]
                else:
                    return self.routing(s_closest_node.routing_table[l][int_val(v2[l])],temp,all_nodes)
            else:
                for node in all_nodes:
                    common_l = common_len(hashValue(node.node_id),hashValue(self.node_id))
                    if (l <=common_l):
                        if (node not in self.intermediate_node and node != s_closest_node):
                            return self.routing(node,temp,all_nodes)
                
                return s_closest_node
                    
    def join(self,d_closest_node,all_nodes):
        
        self.intermediate_node = []
        
        closest_node = self.routing(d_closest_node,'add',all_nodes)
        
        # check if closest_node can be placed in left or right leaf node
        if hashValue(self.node_id) > hashValue(closest_node.node_id):
            # place it in right leaf node
            
            self.right_leaf = sort_nodes(closest_node.right_leaf,closest_node)
            
            #self.right_leaf.append(closest_node)
            # Copying the right leaf
            #for i in range(len(closest_node.right_leaf)):
             #   self.right_leaf.append(closest_node.right_leaf[i])
            
            for i in range(len(closest_node.left_leaf)):
                self.left_leaf.append(closest_node.left_leaf[i])
        
        else:
            self.left_leaf = sort_nodes(closest_node.left_leaf,closest_node)
            # place it in left leaf node
            #self.left_leaf.append(closest_node)
            # Copying the left leaf
            #for i in range(len(closest_node.left_leaf)):
            #    self.left_leaf.append(closest_node.left_leaf[i])
                
            for i in range(len(closest_node.right_leaf)):
                self.right_leaf.append(closest_node.right_leaf[i])
        
        
        if(len(self.right_leaf) > 8):
            self.right_leaf = self.right_leaf[:8]
            
        #print("right = ",len(self.right_leaf))
        
        
        if(len(self.left_leaf) > 8):
            self.left_leaf = self.left_leaf[:8]
            
        #print("left = ",len(self.left_leaf))
        
        
        # update the neighbour_node for the current node (assume that the d_closest_node is the neighbour node)
        self.neighbour_node.append(d_closest_node)
        for i in range (len(d_closest_node.neighbour_node)):
            self.neighbour_node.append(d_closest_node.neighbour_node[i])
        
        if(len(self.neighbour_node) > 32):
            self.neighbour_node = self.neighbour_node[:32]
        
        # update self hash table
        for i in range(len(self.neighbour_node)):
            node_cmp = self.neighbour_node[i]
            l = common_len(hashValue(node_cmp.node_id),hashValue(self.node_id))
            self.routing_table = update_table(self.routing_table,node_cmp.routing_table,l,hashValue(self.node_id))
            
        
        # Update others hash table and leaf nodes
        for i in range(len(self.left_leaf)):
            #print("here = ",hashValue(self.node_id))
            
            self.left_leaf[i].right_leaf = sort_nodes(self.left_leaf[i].right_leaf, self)
        
            #print("right1 = ",len(self.left_leaf[i].right_leaf))
            
        
        for i in range(len(self.right_leaf)):
            self.right_leaf[i].left_leaf = sort_nodes(self.right_leaf[i].left_leaf, self)
        
            #print("left1 = ",len(self.right_leaf[i].left_leaf))
        
        for i in range(len(self.left_leaf)):
            l = common_len(hashValue(self.left_leaf[i].node_id),hashValue(self.node_id))
            self.left_leaf[i].routing_table = update_table(self.left_leaf[i].routing_table,self.routing_table,l,hashValue(self.left_leaf[i].node_id))
        
        for i in range(len(self.right_leaf)):
            l = common_len(hashValue(self.right_leaf[i].node_id),hashValue(self.node_id))
            self.right_leaf[i].routing_table = update_table(self.right_leaf[i].routing_table,self.routing_table,l,hashValue(self.right_leaf[i].node_id))
        
        for i in range(32):
            for j in range(16):
                if (self.routing_table[i][j]!=None and self.routing_table[i][j].node_id != self.node_id):
                    l = common_len(hashValue(self.routing_table[i][j].node_id),hashValue(self.node_id))
                    self.routing_table[i][j].routing_table = update_table(self.routing_table[i][j].routing_table,self.routing_table,l,hashValue(self.routing_table[i][j].node_id))
        
        # Some print statments
        #closest_node.print_routing_table()
        #print(self.intermediate_node)
        
            
    def print_routing_table(self):
        
        
        
        for i in range(len(self.routing_table)):
            for k in self.routing_table[i]:
                if k != None:
                    print(hashValue(k.node_id),end=" ")
                else:
                    print(k,end=" ")
            print()
           
        print("\n left leaf : ",end=" ")
        
        for i in range(len(self.left_leaf)):
            print(hashValue(self.left_leaf[i].node_id),end = "  ")
        
        print("\n right leaf : ",end=" ")
        
        for i in range(len(self.right_leaf)):
            print(hashValue(self.right_leaf[i].node_id),end = "  ")
            
        print()
        
def delete_node(node, all_nodes):
    
    for i in all_nodes:
        
        if i.node_id == node.node_id:
            continue
            
        else:
            '''if node in i.left_leaf:
                for j in range(len(i.left_leaf)):
                    if i.left_leaf[j].node_id == node.node_id:
                        if (len(i.left_leaf[0].left_leaf)>=1):
                            if i.left_leaf[0].left_leaf[-1] not in i.left_leaf:
                                i.left_leaf[j] = i.left_leaf[0].left_leaf[-1]
                        else:
                            i.left_leaf.remove(i.left_leaf[j])
                        break

            if node in i.right_leaf:
                for j in range(len(i.right_leaf)):
                    if i.right_leaf[j] == node:
                        if (len(i.right_leaf[0].right_leaf)>=1):
                            if i.right_leaf[0].right_leaf[-1] not in i.right_leaf:
                                i.right_leaf[j] = i.right_leaf[0].right_leaf[-1]
                        else:
                            i.right_leaf.remove(i.right_leaf[j])
                        break'''
                    
            for j in range(32):
                for k in range(16):
                    if i.routing_table[j][k]==node:
                        kk = False
                        for n in all_nodes:
                            if n != node :
                                common_l = common_len(hashValue(n.node_id),hashValue(i.node_id))
                                #if (common_l>=j and hashValue(n.node_id)[j]==str_value(k) and hashValue(i.node_id)[j]==str_value(k) ):
                                if (common_l>=j and hashValue(n.node_id)[j]==str_value(k)):
                                    i.routing_table[j][k] = n
                                    kk = True
                        if kk == False:
                            i.routing_table[j][k] = None
                                
            if node in i.neighbour_node:
                i.neighbour_node.remove(node)

def routing_data(current_node,final_node_id,all_nodes,cn,lf):
    
    #print("comp_val :",hashValue(current_node.node_id))
    #print("value :",final_node_id)
    if hashValue(current_node.node_id) == final_node_id:
        return cn

    # If the node is in range of leaf node
    elif len(current_node.left_leaf)!=0 and len(current_node.right_leaf)!=0 and  hashValue(current_node.right_leaf[0].node_id) <= final_node_id and hashValue(current_node.left_leaf[-1].node_id) >= final_node_id :
            
        closest_id = hashValue(current_node.node_id)
        closest_node = current_node
        
        for node in current_node.left_leaf:
            if closest_id >= final_node_id:
                closest_id = final_node_id
                closest_node = node
            
        for node in current_node.right_leaf:
            if closest_id >= final_node_id:
                closest_id = final_node_id
                closest_node = node
        
        return cn
        #return closest_node
    
    elif len(current_node.left_leaf)!=0 and len(current_node.right_leaf)==0 and  hashValue(current_node.left_leaf[0].node_id) <= final_node_id and hashValue(current_node.left_leaf[-1].node_id) >= final_node_id :
            
        closest_id = hashValue(current_node.node_id)
        closest_node = current_node
            
        for node in current_node.left_leaf:
            if closest_id >= final_node_id:
                closest_id = final_node_id
                closest_node = node
            
        return cn
        #return closest_node
            
    elif len(current_node.left_leaf)==0 and len(current_node.right_leaf)!=0 and  hashValue(current_node.right_leaf[0].node_id) <= final_node_id and hashValue(current_node.right_leaf[-1].node_id) >= final_node_id :

        closest_id = hashValue(current_node.node_id)
        closest_node = current_node

        for node in current_node.right_leaf:
            if closest_id >= final_node_id:
                closest_id = final_node_id
                closest_node = node

        return cn

    else:
        l = 0
        v1 = hashValue(current_node.node_id)
        v2 = final_node_id

        for i in range(32):
            if(v1[i]==v2[i]):
                l+=1
            else:
                break
        
        if(current_node.routing_table[l][int_val(v2[l])] != None):
            if current_node.routing_table[l][int_val(v2[l])] not in lf:
                lf.append(current_node.routing_table[l][int_val(v2[l])])
                return routing_data(current_node.routing_table[l][int_val(v2[l])],final_node_id,all_nodes,cn+1,lf)
            else:
                for node in all_nodes:
                    common_l = common_len(hashValue(node.node_id),final_node_id)
                    if (l < common_l):
                        lf.append(node)
                        return routing_data(node,final_node_id,all_nodes,cn+1,lf)
                    
                return cn
        else:
            for node in all_nodes:
                common_l = common_len(hashValue(node.node_id),final_node_id)
                if (l < common_l):
                    lf.append(node)
                    return routing_data(node,final_node_id,all_nodes,cn+1,lf)
                    
            return cn
                    

node_cnt = sys.argv[1]
lis = []
data_lis_head = []
data_lis = {}
tot_search = 0
tot_node_del = 0
for idx,i in enumerate(randomGenerator(int(node_cnt))):
    #print(idx+1,") ",i,end=" - ")
    #print(hashValue(str(i)))

    if idx == 0:
        lis.append(Pastry_Node(str(i),i,(i*(i+1))%20000,lis))
    else:
        k = smallest_dis(i,i+1,lis)
        #print(k.node_id)
        lis.append(Pastry_Node(str(i),i,(i*(i+1))%20000,lis,k))
print("## ",node_cnt," Nodes are created\n")
while(True):
    
    opt = input("1 : Exit\n2 : Delete Nodes\n3 : Add data elements\n4 : Print Node details\n5 : Lookup Queries\n## ")
    
    
    if opt == "1":
        break
        
    # delete a node
    elif opt == "2":
        del_cnt = int(input("## How many nodes to delete : "))
        tot_node_del = del_cnt
        if (int(del_cnt)<=len(lis)):
            i=0
            add_del_data = []
            while(i<del_cnt):
                print("deleting : node  ",hashValue(lis[0].node_id))
                delete_node(lis[0], lis)
                
                #ii = randomGenerator(1)[0] % len(lis)
                
                for j in range(len(lis[0].data_element)):
                    #lis[ii].add_element(lis[0].data_element[j]) 
                    #data_lis[lis[0].data_element[j]]=lis[ii].node_id
                    #ii=(ii+1)%len(lis)
                    add_del_data.append(lis[0].data_element[j])
                lis.remove(lis[0])
                
                i+=1
            
            ii = randomGenerator(1)[0] % len(lis)
            for j in range(len(add_del_data)):
                if (ii == 0):
                    ii+=1
                lis[ii].add_element(add_del_data[j])
                data_lis[add_del_data[j]]=lis[ii].node_id
                ii=(ii+1)%len(lis)
        else:
            print("## Network contain ",len(lis)," nodes only")
                        
        #print(lis)
        
    elif opt == "3":
        ele_cnt = input("## How many elements to distribute : ")
        ii = 0
        for idx,i in enumerate(randomGenerator(int(ele_cnt))):
            lis[ii].add_element(hashValue(str(idx)))
            data_lis[hashValue(str(idx))]=lis[ii].node_id
            data_lis_head.append(hashValue(str(idx)))
            ii=(ii+1)%len(lis)
    elif opt == "4":
        print("Select the node id from the given list :")
        for i in range(len(lis)):
            print(lis[i].node_id, end = " , ")
        node_id = input("\n## ")
        print("Hash value of ", node_id ," = ",hashValue(node_id))
        
        temp = False
        for i in range(len(lis)):
            if lis[i].node_id == node_id:
                temp = True
                print("\nNetwork Details :")
                print("Total number of nodes : ",len(lis))
                print("Total number of data elements : ",len(data_lis)) 
                print("Total search queries : ",tot_search)
                print("Total node add queries : ",lis[0].tot_node_add)
                print("Total node delete queries : ",tot_node_del)
                print("Total data add queries : ",len(data_lis))
                
                print("\nRouting table ",node_id,":",hashValue(str(node_id)))
                
                lis[i].print_routing_table()
                break
                
         
    elif opt == "5":
        tot_search = int(input("Enter the total Number of lookup queries : "))
        li = []
        c = 1
        p = 0
        #print(data_lis_head)
        for i in randomGenerator2(tot_search):
            #print(c)
            kk = i % len(data_lis_head)
            li.append(routing_data(lis[0],hashValue(data_lis[data_lis_head[kk]]),lis,1,[]))
            
            if(c == 10000):
                p=p+1
                print(p," * 10000 is done")
                c=1
            else:
                c+=1
                
        cnt_tot =0
        for i in li:
            cnt_tot+=i
        
        print("Average number of hops for a search query = ",cnt_tot/tot_search)
        
        
        test_cnt = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        
        for i in range(len(li)):
            test_cnt[li[i]]+=1
        
        for i in range(len(test_cnt)):
            print(i," : ",test_cnt[i])
    else : 
        print("## Please choose right option : ")
    #delete_node(lis[0], lis)