from open_system_one.primitives import BloomPrefilter,CapabilityIssuer,GSet,LamportClock,candidate_scores,compose,content_id,fold_monoid,memoize,reify,unify,UnificationError

def test_reification_and_composition():
    c=reify(3,lambda x:x+2); assert c.continue_(c.value)==5
    assert compose(lambda x:x+1,lambda x:x*2)(3)==8

def test_unification():
    assert unify(("?x","b"),("a","b"))=={"?x":"a"}
    with __import__("pytest").raises(UnificationError): unify("a","b")

def test_memoization_uses_canonical_identity():
    calls={"n":0}
    @memoize
    def f(x): calls["n"]+=1; return x["a"]
    assert f({"a":3,"b":4})==3 and f({"b":4,"a":3})==3 and calls["n"]==1

def test_bloom_filter_is_never_negative_for_inserted_value():
    b=BloomPrefilter(); b.add("x"); assert b.maybe_contains("x")

def test_monoid_clock_hash_capability_crdt_and_scoring():
    assert fold_monoid([1,2,3],lambda a,b:a+b,0)==6
    c=LamportClock(); t=c.tick(); assert c.receive(t)>t
    assert content_id({"a":1,"b":2})==content_id({"b":2,"a":1})
    issuer=CapabilityIssuer(b"s"); cap=issuer.issue("a","read","r")
    assert issuer.verify(cap,"a","read","r") and not issuer.verify(cap,"a","write","r")
    assert GSet().add("a").merge(GSet().add("b"))==GSet(frozenset({"a","b"}))
    assert candidate_scores([1,0],{"a":[1,0],"b":[0,1]})["a"]>candidate_scores([1,0],{"a":[1,0],"b":[0,1]})["b"]
