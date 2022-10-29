#include<fstream>
#include<iostream>
#include<string>
#include<map>
#include<vector>
#include<algorithm>

int config_length;
std::ifstream fin;
std::ofstream fout;

int cmp(const std::pair<std::string, int>& x, const std::pair<std::string, int>& y)  
{  
	return x.second < y.second;  
}  

void sortMapByValue(std::map<std::string, int>& tMap,std::vector<std::pair<std::string, int> >& tVector)  
{  
	for (std::map<std::string, int>::iterator curr = tMap.begin(); curr != tMap.end(); curr++){   
		tVector.push_back(make_pair(curr->first, curr->second));    
    }
	sort(tVector.begin(), tVector.end(), cmp);  
}  

std::string purify(std::string s)
{
    int f=0,t=s.length()-1;
    std::string new_s;
    while(1){
        if (('A'<=s[f] && s[f] <= 'Z')||('a'<=s[f] && s[f] <= 'z')) break;
        else f++;   
        if(f>s.length()) return "-1";
    }
    while(1){
        if (('A'<=s[t] && s[t] <= 'Z')||('a'<=s[t] && s[t] <= 'z')) break;
        else t--;   
        if(t<0) return "-1";
    }
    if (f>t) return "-1";
    new_s = s.substr(f,(t-f+1));
    return new_s;
}

int main()
{
    fin.open("./source/HarryPotter-demo.txt");
    fout.open("./runs/result.txt");
    std::cin >> config_length;
    if(!fin.is_open())
    {
        std::cout << "cannot open the file"<< std::endl;
        return -1;
    }
    std::map<std::string,int>word;
    std::string c;
    char buf[8000000]={0};
    long long int count = 0;
    while (fin >> buf)
    {
        std::string tmp;
        tmp = buf;
        tmp = purify(tmp);
        // std::cout << tmp << std::endl;
        if(tmp == "-1") continue;
        else{
            for(int i = 0; i < tmp.size();i++){
                if('A'<=tmp[i] && tmp[i] <= 'Z'){
                    tmp[i] = tmp[i] - ('A'-'a');
                }
            }
            // std::cout << tmp << std::endl;
        }
        word[tmp]++;
        count ++;
    }
    std::vector<std::pair<std::string,int> > tVector;  
	sortMapByValue(word,tVector);
    int valuetime[11] = {0};
    int count_sort = 0;
    for(int i=0;i<tVector.size();i++){
        if(tVector[i].second < 10) valuetime[tVector[i].second]++;
        if(tVector[i].first.length() >= config_length){
            fout<<tVector[i].first << " "<< tVector[i].first.length() <<": "<<tVector[i].second<<std::endl;
            count_sort++;
        }
    }
    int mintime = 1, flag = 0;
    for(int i=1;i<10;i++){
        if (valuetime[i] == 0 && flag == 0){
            flag = 1;
            mintime++;
        }
        std::cout << "出现" << i << "次的单词有：" << valuetime[i] << "个" << std::endl;
    }
    std::cout << "出现最低次与总单词比例为" << (count_sort*100/count) << "%" << std::endl;
    fin.close();
    fout.close();
    return 0;
}