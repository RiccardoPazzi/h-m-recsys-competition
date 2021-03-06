import implicit
from Recommenders.BaseMatrixFactorizationRecommender import BaseMatrixFactorizationRecommender
from Utils.confidence_scaling import linear_scaling_confidence


class ImplicitALSRecommender(BaseMatrixFactorizationRecommender):
    """ImplicitALSRecommender recommender"""

    RECOMMENDER_NAME = "ImplicitALSRecommender"

    def __init__(self, URM_train, verbose=True):
        super(ImplicitALSRecommender, self).__init__(URM_train=URM_train)
        self.verbose = verbose

    def fit(self,
            factors=100,
            regularization=0.01,
            use_native=True, use_cg=True, use_gpu=False,
            iterations=15,
            calculate_training_loss=False, num_threads=0,
            confidence_scaling=linear_scaling_confidence,
            alpha=1
            ):

        self.rec = implicit.als.AlternatingLeastSquares(factors=factors, regularization=regularization,
                                                        use_native=use_native, use_cg=use_cg, use_gpu=use_gpu,
                                                        iterations=iterations,
                                                        calculate_training_loss=calculate_training_loss,
                                                        num_threads=num_threads)
        if confidence_scaling == None:
            self.rec.fit(linear_scaling_confidence(self.URM_train, **{"alpha": alpha}).T, show_progress=self.verbose)
        else:
            self.rec.fit(confidence_scaling(self.URM_train, **{"alpha": alpha}).T, show_progress=self.verbose)

        self.USER_factors = self.rec.user_factors
        self.ITEM_factors = self.rec.item_factors