#include <iostream>
#include <vector>
#include <cstddef>
#include <set>

#include <gecode/int.hh>
#include <gecode/minimodel.hh>
#include <gecode/search.hh>
using namespace Gecode;


struct Sample { std::vector<std::vector<int>> acc, rej; };

static std::vector<std::vector<int>> read_block(std::istream& in) {
    std::size_t n; if (!(in >> n)) return {};
    std::vector<std::vector<int>> v(n);
    for (std::size_t i = 0; i < n; ++i) {
        std::size_t len; in >> len; v[i].resize(len);
        for (std::size_t j = 0; j < len; ++j) in >> v[i][j];
    }
    return v;
}
static Sample read_instance(std::istream& in) {
    Sample s; s.acc = read_block(in); s.rej = read_block(in); return s; }


static int upper_bound_states(const Sample& M){
    std::set<std::vector<int>> pref; auto add=[&](const auto& V){
        for(const auto& w:V){ std::vector<int> p; pref.insert(p);
            for(int b:w){ p.push_back(b); pref.insert(p);} }
    }; add(M.acc); add(M.rej); return (int)pref.size(); }


class DFAspace: public Space{
public:
    IntVarArray T0,T1; BoolVarArray A; IntVarArray S;

    DFAspace(const Sample& M,int N):
        T0(*this,N,0,N-1),T1(*this,N,0,N-1),A(*this,N,0,1){
        struct Word{std::size_t off,len; const std::vector<int>* w; bool mustAcc;};
        std::vector<Word> words; std::size_t total=0;
        auto collect=[&](const std::vector<std::vector<int>>& V,bool acc){
            for(const auto& w:V){ words.push_back({total,w.size(),&w,acc}); total+=w.size()+1; }
        };
        collect(M.acc,true); collect(M.rej,false);
        S = IntVarArray(*this,total,0,N-1);

        for(const Word& wd: words){
            std::size_t o=wd.off,L=wd.len; const auto& w=*wd.w;
            rel(*this,S[o]==0);
            for(std::size_t j=0;j<L;++j){
                const IntVar& cur=S[o+j]; const IntVar& nxt=S[o+j+1];
                element(*this, (w[j]?T1:T0), cur, nxt);
            }
            BoolVar accLast(*this,0,1);
            element(*this,A,S[o+L],accLast);
            rel(*this, accLast == (wd.mustAcc?1:0));
        }
        IntArgs ord(N); for(int q=0;q<N;++q) ord[q]=q; precede(*this,S,ord);
        branch(*this,S ,INT_VAR_SIZE_MIN(),INT_VAL_MIN());
        branch(*this,T0,INT_VAR_NONE()   ,INT_VAL_MIN());
        branch(*this,T1,INT_VAR_NONE()   ,INT_VAL_MIN());
        branch(*this,A ,BOOL_VAR_NONE()  ,BOOL_VAL_MIN());
    }

    DFAspace(DFAspace& s):Space(s){ T0.update(*this,s.T0); T1.update(*this,s.T1);
        A.update(*this,s.A); S.update(*this,s.S);} Space* copy(void) override
        {return new DFAspace(*this);} };

int main(){ std::ios::sync_with_stdio(false); std::cin.tie(nullptr);
    const Sample inst=read_instance(std::cin);
    if(inst.acc.empty()&&inst.rej.empty()) return 0;
    const int UB=upper_bound_states(inst);
    for(int N=1;N<=UB;++N){
        DFAspace* root=new DFAspace(inst,N);
        DFS<DFAspace> dfs(root); delete root;
        if(DFAspace* sol=dfs.next()){
            std::cout<<inst.acc.size()<<'\n';
            for(const auto& w:inst.acc){ std::cout<<w.size(); for(int b:w) std::cout<<' '<<b; std::cout<<'\n'; }
            std::cout<<inst.rej.size()<<'\n';
            for(const auto& w:inst.rej){ std::cout<<w.size(); for(int b:w) std::cout<<' '<<b; std::cout<<'\n'; }
            std::cout<<N<<'\n';
            for(int q=0;q<N;++q)
                std::cout<<sol->T0[q].val()<<' '<<sol->T1[q].val()<<' '<<sol->A[q].val()<<'\n';
            delete sol; return 0; }
    }
    return 0; }
