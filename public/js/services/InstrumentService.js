function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function list_comp(list, attr){
    var ret = [];
    for (ele in list){
        ret.push(list[ele][attr]);
    }
    return ret;
}

function next_question_id(questions){
    var last = 0;
    for (q in questions){
        var q_id = parseInt(questions[q].question_id);
        if (last < q_id){
            last = q_id;
        }
    }
    return last+1;
}

function check_dups(questions){
    q_ids = list_comp(questions, 'question_id')
    counter = {}
    faulty = [];
    for (index in questions){
        var q_id = questions[index].question_id;
        if (! counter.hasOwnProperty(q_id) ){
            counter[q_id] = 0;
        }
        counter[q_id] += 1;
    }
    for (q_id in counter){
        if(counter[q_id] > 1){
            faulty.push(q_id);
        }
    }
    return faulty;
}

app = angular.module('eda.instrument_service', ['eda.config']);

    app.service('InstrumentService', ['$http','$rootScope', 'EdaConfig', function($http, $rootscope, eConfig){
        this.preview_server = eConfig.preview_server;
        var api_domain = '/api/ajax/v/'

        this.init = function(){
            this.current = {
                name: 'Loading...',
                urlname: 'eda5',
                description: 'Loading...',
                questions: [],
                version:{
                    major: '1',
                    minor: 'current',
                },
                language: 'en'
            };
            var bookmark = localStorage.getItem('bookmark');
            console.debug('Bookmark Found' + bookmark);
            if (bookmark){
                bookmark = JSON.parse(bookmark);
                this.current.version.major = bookmark.major;
                this.current.version.minor = 'current';
            }

            this.all_questionnaires = [
                this.current,
            ];
            this.setCurrent(this.current, this.current.version);
        }

        this.bc_instrument = function(){
            $rootscope.$broadcast('change_instrument');
            $rootscope.$broadcast('change_card');
        }

        this.bc_card = function(){
            $rootscope.$broadcast('change_card');
        }

        this.initInstrument = function(instrument){
            iservice.current = instrument;
            this.current = instrument;
            this.cardtype = 'prelims';
            this.card = this.current;
            this.bc_instrument();
        }


        var iservice = this;

        this.fetch_all_questionnaires = function(){
            prom = $http.get(api_domain+'list.json')
                .success(function(data){
                    iservice.all_questionnaires = data.versions;
                    iservice.perms = data.perms;
                    $rootscope.$broadcast('update_questionnaires');
                    console.info("Fetched Questionnaires!");
                })
                .error(function(err){
                    console.info('error');
                    console.info(err);
                });
            return prom;
        };


        this.fetch_instrument = function(instrument, version){
            var url = api_domain + 'fetch/'+version.major+'/current/'+instrument.urlname+'.json'
            prom = $http.post(url)
            .success(function(data){
                iservice.current_perms = data.perms;
                iservice.initInstrument(data.questionnaire);
            })
            .error(function(err){
                console.info(err);
            });
            return prom;
        };

        this.save_instrument = function(versiontype, version){
            var current = iservice.current;
            $rootscope.$broadcast('auth_set_timeout');

            if (version){
                current.version.description = version.description;
                current.version.shortname = version.shortname;
            }
            var dups = check_dups(current.questions);
            if (dups.length >= 1){
                $rootscope.$broadcast('error_duplicate_questions', dups);
                return;
            }
            var url = api_domain + 'save/'+versiontype;

            var payload = {
                questionnaire: iservice.current
            };

            var resp = $http.post(url, payload);
            resp.success(function(new_version){
                iservice.current.version = new_version;

                bookmark = {
                    'major': new_version.major,
                    'minor': new_version.minor
                };

                localStorage.setItem('bookmark', JSON.stringify(bookmark));
                iservice.fetch_all_questionnaires();
                iservice.bc_instrument();
            });

            resp.error(function(data, status){
                console.info(status, data);
                $rootscope.$broadcast('permission_denied', data);
            });
        };

        this.delete_version = function(){
            id = iservice.current.instrument_id;
            major = iservice.current.version.major;
            minor = iservice.current.version.minor;
            var url = api_domain + 'delete/' + id + '/' + major + '/' + minor;
            console.info("Deleting current version: ",iservice.current);
            var prom = $http.get(url);
            prom.success(function(data){
                iservice.setCurrent(iservice.current, iservice.current.version);
            });
            prom.error(function(data, status){
                console.info("FAILED TO DELETE "+ status);
            });

        };

        this.setCurrent = function(instrument, version){
            prom = this.fetch_instrument(instrument, version);
            prom.success(function(data){
                iservice.initInstrument(data.questionnaire);
            });
        };

        this.setCard = function(cardtype, card){
            $rootscope.$broadcast('auth_set_timeout');

            this.cardtype = cardtype;
            if (cardtype == 'prelims'){
                this.card = this.current;
            }
            else{
                this.card = card;
            }
            this.bc_card();
        };

        this.addQuestion = function(){
            $rootscope.$broadcast('auth_set_timeout');

            var next_id = next_question_id(iservice.current.questions);
            var blank_question = {
                instrument_id: iservice.current.instrument_id,
                section_label: '',
                probe_text: '',
                symptom_text: '',
                short_name: 'none',
                question_id: next_id,
                rules: [],
                answers: [],
                section_label: '',
                deleted_on: null,
                created_on: Date.now(),
                initial: false
            };

            iservice.current.questions.push(blank_question);
            iservice.setCard('question', blank_question);
        };

        this.deleteQuestion = function(question){
            $rootscope.$broadcast('auth_set_timeout');

            var index = iservice.current.questions.indexOf(question);
            iservice.current.questions.splice(index, 1);
            this.bc_instrument();
        }

        $rootscope.$on('save_current_questionnaire', function(evt){
            iservice.save_instrument('minor');
        });

        $rootscope.$on('save_version_questionnaire', function(evt, version){
//			iservice.save_instrument('major', version);
            iservice.save_instrument('major', version);
        });

        $rootscope.$on('delete_current_version', function(evt, version){
            iservice.delete_version();
        });
        $rootscope.$on('delete_question', function(evt, question){
            iservice.deleteQuestion(question);
        });


        this.init();

    }]);





