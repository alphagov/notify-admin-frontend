from app.notify_client import NotifyAdminAPIClient, cache


class LetterJobsClient(NotifyAdminAPIClient):
    @cache.delete_by_pattern("service-????????-????-????-????-????????????-returned-letters-statistics")
    @cache.delete_by_pattern("service-????????-????-????-????-????????????-returned-letters-summary")
    def submit_returned_letters(self, references):
        return self.post(url="/letters/returned", data={"references": references})


letter_jobs_client = LetterJobsClient()
